import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN, DP_CODES, scale_value

_LOGGER = logging.getLogger(__name__)

class TankQualCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client, device_id: str, scan_seconds: int):
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_coordinator",
            update_interval=timedelta(seconds=scan_seconds),
        )
        self._client = client
        self._device_id = device_id

    async def _async_update_data(self):
        raw = await self._client.fetch_properties(self._device_id)
        out = {}
        for code in DP_CODES.keys():
            if code in raw:
                out[code] = scale_value(code, raw[code])
        return out
