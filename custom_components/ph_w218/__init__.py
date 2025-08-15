from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS, CONF_ENDPOINT, CONF_CLIENT_ID, CONF_CLIENT_SECRET, CONF_DEVICE_ID, CONF_PREFIX, CONF_SCAN_INTERVAL, DEFAULT_PREFIX, DEFAULT_SCAN
from .api import TuyaWaterClient
from .coordinator import TankQualCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    data = entry.data
    opts = entry.options

    endpoint = data[CONF_ENDPOINT]
    client_id = data[CONF_CLIENT_ID]
    client_secret = data[CONF_CLIENT_SECRET]
    device_id = data[CONF_DEVICE_ID]
    prefix = data.get(CONF_PREFIX, DEFAULT_PREFIX)
    scan = int(opts.get(CONF_SCAN_INTERVAL, data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN)))

    client = TuyaWaterClient(hass, endpoint, client_id, client_secret)
    coordinator = TankQualCoordinator(hass, client, device_id, scan)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }

    entry.async_on_unload(entry.add_update_listener(_options_update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def _options_update_listener(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
