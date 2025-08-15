from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN, PLATFORMS,
    CONF_ENDPOINT, CONF_CLIENT_ID, CONF_CLIENT_SECRET, CONF_DEVICE_ID,
    CONF_PREFIX, CONF_SCAN_INTERVAL, DEFAULT_PREFIX, DEFAULT_SCAN,
)

class TankQualConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            if not user_input[CONF_ENDPOINT].startswith("http"):
                errors["base"] = "endpoint"
            if not errors:
                return self.async_create_entry(title="ph_w218 Integration by CrossboxLabs", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_ENDPOINT, default="https://openapi.tuyaeu.com"): str,
            vol.Required(CONF_CLIENT_ID): str,
            vol.Required(CONF_CLIENT_SECRET): str,
            vol.Required(CONF_DEVICE_ID): str,
            vol.Optional(CONF_PREFIX, default=DEFAULT_PREFIX): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN): int,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return TankQualOptionsFlow(config_entry)

class TankQualOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry):
        self._entry = entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        data = {**self._entry.data, **self._entry.options}
        schema = vol.Schema({
            vol.Optional(CONF_PREFIX, default=data.get(CONF_PREFIX, DEFAULT_PREFIX)): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN)): int,
        })
        return self.async_show_form(step_id="init", data_schema=schema)
