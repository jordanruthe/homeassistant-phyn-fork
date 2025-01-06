"""Support for Phyn Water Monitor sensors."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN as PHYN_DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flo sensors from config entry."""
    coordinator = hass.data[PHYN_DOMAIN]["coordinator"]
    entities = []
    for device in coordinator.devices:
        entities.extend([
            entity
            for entity in device.entities
            if isinstance(entity, SensorEntity)
        ])
    async_add_entities(entities)
