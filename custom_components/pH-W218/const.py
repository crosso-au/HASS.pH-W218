DOMAIN = "pH-W218"
PLATFORMS = ["sensor"]

CONF_ENDPOINT = "endpoint"
CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"
CONF_DEVICE_ID = "device_id"
CONF_PREFIX = "name_prefix"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_PREFIX = "pHW218"
DEFAULT_SCAN = 60  # seconds

# Tuya DP codes we care about
DP_CODES = {
    "temp_current": {"name": "Temperature", "icon": "mdi:thermometer", "unit": "°C"},
    "ph_current": {"name": "pH", "icon": "mdi:flask-outline", "unit": "pH"},
    "tds_current": {"name": "TDS", "icon": "mdi:cup-water", "unit": "ppm"},
    "ec_current": {"name": "EC", "icon": "mdi:sine-wave", "unit": "µS/cm"},
    "salinity_current": {"name": "Salt", "icon": "mdi:waves", "unit": "ppm"},
    "orp_current": {"name": "ORP", "icon": "mdi:flash-outline", "unit": "mV"},
    "cf_current": {"name": "CF", "icon": "mdi:chart-line", "unit": None},
    "pro_current": {"name": "Proportion", "icon": "mdi:scale-balance", "unit": None},
    "rh_current": {"name": "RH", "icon": "mdi:water-percent", "unit": "%"}
}

def scale_value(code: str, raw):
    if raw is None:
        return None
    if code == "temp_current":
        return round(raw / 10.0, 1)      # 194 -> 19.4 °C
    if code == "ph_current":
        return round(raw / 100.0, 2)     # 721 -> 7.21 pH
    if code == "tds_current":
        return int(raw)                   # ppm
    if code == "ec_current":
        return int(raw)                   # µS/cm
    if code == "salinity_current":
        return int(raw)                   # ppm
    if code == "orp_current":
        return int(raw)                   # mV
    if code == "cf_current":
        return round(raw / 100.0, 2)      # 142 -> 1.42
    if code == "pro_current":
        return round(raw / 1000.0, 3)     # 999 -> 0.999
    if code == "rh_current":
        return int(raw)                   # %
    return raw
