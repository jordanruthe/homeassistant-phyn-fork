""" Generic Phyn Device"""

from typing import Any
from ..const import LOGGER

class PhynDevice:
    """Generice Phyn Device"""
    def __init__ (self, coordinator, home_id: str, device_id: str, product_code: str) -> None:
        self._coordinator = coordinator
        self._phyn_home_id: str = home_id
        self._phyn_device_id: str = device_id
        self._product_code: str = product_code
        self._manufacturer: str = "Phyn"
        self._device_state: dict[str, Any] = {}
        self._device_preferences: dict[dict[str, Any]] = {}
        self._firmware_info: dict[str, Any] = {}
        self._update_count = 0
    
    @property
    def available(self) -> bool:
        """Return True if device is available."""
        return self._device_state["online_status"]["v"] == "online"
    
    @property
    def coordinator(self):
        """Return update coordinator"""
        return self._coordinator

    @property
    def device_name(self) -> str:
        """Return device name."""
        return f"{self.manufacturer} {self.model}"

    @property
    def firmware_has_update(self) -> bool:
        """Return if the firmware has an update"""
        if "fw_version" not in self._firmware_info:
            return None
        return int(self._firmware_info["fw_version"]) > int(self._device_state["fw_version"])

    @property
    def firmware_latest_version(self) -> str | None:
        """Return the latest available firmware version"""
        if "fw_version" not in self._firmware_info:
            return None
        return self._firmware_info["fw_version"]

    @property
    def firmware_release_url(self) -> str | None:
        """Return the URL for the latest release notes"""
        if "release_notes" not in self._firmware_info:
            return None
        return self._firmware_info["release_notes"]

    @property
    def firmware_version(self) -> str:
        """Return the firmware version for the device."""
        return self._device_state["fw_version"]

    @property
    def home_id(self) -> str:
        """Return Phyn home id."""
        return self._phyn_home_id

    @property
    def id(self) -> str:
        """Return Phyn device id."""
        return self._phyn_device_id

    @property
    def manufacturer(self) -> str:
        """Return manufacturer for device."""
        return self._manufacturer

    @property
    def model(self) -> str:
        """Return model for device."""
        return self._device_state["product_code"]

    @property
    def rssi(self) -> float:
        """Return rssi for device."""
        return self._device_state["signal_strength"]

    @property
    def serial_number(self) -> str:
        """Return the serial number for the device."""
        return self._device_state["serial_number"]
    
    async def async_setup(self):
        pass

    async def _update_firmware_information(self, *_) -> None:
        self._firmware_info.update(
            (await self._coordinator.api_client.device.get_latest_firmware_info(self._phyn_device_id))[0]
        )
        LOGGER.debug("%s firmware: %s", self.device_name, self._firmware_info)

    async def _update_device_state(self, *_) -> None:
        """Update the device state from the API."""
        self._device_state.update(await self._coordinator.api_client.device.get_state(
            self._phyn_device_id
        ))
        #LOGGER.debug("Phyn device state: %s", self._device_state)
