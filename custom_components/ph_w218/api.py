import hmac, hashlib, time, uuid
from typing import Dict, Any, Optional

class TuyaWaterClient:
    def __init__(self, hass, endpoint: str, client_id: str, client_secret: str):
        from homeassistant.helpers.aiohttp_client import async_get_clientsession
        self._hass = hass
        self._session = async_get_clientsession(hass)
        self._endpoint = endpoint.rstrip("/")
        self._client_id = client_id
        self._secret = client_secret

        self._access_token: Optional[str] = None
        self._token_expire_epoch: float = 0.0  # epoch seconds

    @staticmethod
    def _now_ms() -> str:
        return str(int(time.time() * 1000))

    @staticmethod
    def _nonce() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def _sha256_hex(s: str) -> str:
        h = hashlib.sha256()
        h.update(s.encode("utf-8"))
        return h.hexdigest()

    def _sign(self, method: str, path: str, body: str, t: str, nonce: str, access_token: Optional[str] = None) -> str:
        empty_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        content_sha256 = self._sha256_hex(body) if body else empty_hash
        string_to_sign = f"{method}\n{content_sha256}\n\n{path}"
        base = self._client_id + (access_token or "") + t + nonce + string_to_sign if access_token else self._client_id + t + nonce + string_to_sign
        return hmac.new(self._secret.encode("utf-8"), base.encode("utf-8"), hashlib.sha256).hexdigest().upper()

    async def _get_json(self, url: str, headers: Dict[str, str]):
        async with self._session.get(url, headers=headers, timeout=20) as resp:
            try:
                j = await resp.json()
            except Exception:
                j = {"success": False, "status": resp.status, "raw": await resp.text()}
            j["_status"] = resp.status
            return j

    async def _ensure_token(self) -> str:
        now = time.time()
        if self._access_token and now < self._token_expire_epoch - 60:
            return self._access_token

        t = self._now_ms()
        nonce = self._nonce()
        method = "GET"
        path = "/v1.0/token?grant_type=1"
        sign = self._sign(method, path, "", t, nonce, None)
        headers = {
            "client_id": self._client_id,
            "sign": sign,
            "t": t,
            "sign_method": "HMAC-SHA256",
            "nonce": nonce,
        }
        j = await self._get_json(f"{self._endpoint}{path}", headers)
        if j.get("success") and j.get("_status") == 200:
            res = j.get("result", {})
            self._access_token = res.get("access_token")
            expire = res.get("expire_time") or res.get("expires_in")
            if expire:
                if int(expire) > 1_000_000_000:
                    self._token_expire_epoch = int(expire) / 1000.0
                else:
                    self._token_expire_epoch = time.time() + int(expire)
            else:
                self._token_expire_epoch = time.time() + 3600
            return self._access_token
        raise RuntimeError(f"Token error: {j}")

    async def fetch_properties(self, device_id: str) -> Dict[str, Any]:
        token = await self._ensure_token()
        t = self._now_ms()
        nonce = self._nonce()
        method = "GET"
        path = f"/v2.0/cloud/thing/{device_id}/shadow/properties"
        sign = self._sign(method, path, "", t, nonce, token)
        headers = {
            "client_id": self._client_id,
            "sign": sign,
            "t": t,
            "sign_method": "HMAC-SHA256",
            "nonce": nonce,
            "access_token": token,
            "Content-Type": "application/json",
        }
        j = await self._get_json(f"{self._endpoint}{path}", headers)
        if j.get("success") and j.get("_status") == 200 and "result" in j:
            props = j["result"].get("properties", [])
            return {p.get("code"): p.get("value") for p in props if "code" in p}
        raise RuntimeError(f"Props error: {j}")
