from __future__ import annotations
import logging
from dataclasses import dataclass
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, CONF_DEVICE_ID, CONF_PREFIX
from .coordinator import TankQualCoordinator

_LOGGER = logging.getLogger(__name__)

@dataclass
class TankQualDesc:
    code: str
    name: str
    unit: str | None
    icon: str

DESCS: list[TankQualDesc] = [
    TankQualDesc("temp_current", "Temperature", "°C", "mdi:thermometer"),
    TankQualDesc("ph_current", "pH", "pH", "mdi:flask-outline"),
    TankQualDesc("tds_current", "TDS", "ppm", "mdi:cup-water"),
    TankQualDesc("ec_current", "EC", "µS/cm", "mdi:sine-wave"),
    TankQualDesc("salinity_current", "Salt", "ppm", "mdi:waves"),
    TankQualDesc("orp_current", "ORP", "mV", "mdi:flash-outline"),
    TankQualDesc("cf_current", "CF", None, "mdi:chart-line"),
    TankQualDesc("pro_current", "Proportion", None, "mdi:scale-balance"),
    TankQualDesc("rh_current", "RH", "%", "mdi:water-percent"),
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    data = hass.data[DOMAIN][entry.entry_id]
    coord: TankQualCoordinator = data["coordinator"]
    prefix = entry.data.get(CONF_PREFIX)
    device_id = entry.data.get(CONF_DEVICE_ID)
    entities: list[TankQualSensor] = []

    for d in DESCS:
        unique_id = f"{device_id}_{d.code}"
        name = f"{prefix} - {d.name}"
        entities.append(TankQualSensor(coord, unique_id, name, d.code, d.unit, d.icon, device_id))
    async_add_entities(entities)

class TankQualSensor(CoordinatorEntity[TankQualCoordinator], SensorEntity):
    _attr_has_entity_name = False
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, unique_id: str, name: str, code: str, unit: str | None, icon: str, device_id: str):
        super().__init__(coordinator)
        self._attr_unique_id = unique_id
        self._attr_name = name
        self._code = code
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._device_id = device_id
         # Add your image here
        self._attr_entity_picture = "/local/pH-W218/logo.png"
    @property
    def native_value(self):
        return self.coordinator.data.get(self._code) if self.coordinator.data else None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": "Analytical Labs Integration by CrossboxLabs",
            "manufacturer": "CrossboxLabs",
            "model": "pH-W218",
        }
