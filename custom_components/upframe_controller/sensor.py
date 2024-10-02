import requests
from homeassistant.components.sensor import SensorEntity
from . import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the display status sensor."""
    url = hass.data[DOMAIN][config_entry.entry_id]["url"]
    async_add_entities([DisplayStatusSensor(url)])

class DisplayStatusSensor(SensorEntity):
    """Representation of the display status sensor."""

    def __init__(self, url):
        self._name = "Display Status"
        self._state = None
        self._url = url

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Fetch the display status from the server."""
        try:
            response = requests.get(f"{self._url}/system/display_status")
            if response.status_code == 200:
                self._state = response.json().get("display_on")
        except Exception as e:
            self._state = None