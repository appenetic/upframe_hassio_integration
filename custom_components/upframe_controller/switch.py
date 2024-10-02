import requests
from homeassistant.components.switch import SwitchEntity
from . import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the display control switch."""
    url = hass.data[DOMAIN][config_entry.entry_id]["url"]
    async_add_entities([DisplaySwitch(url)])

class DisplaySwitch(SwitchEntity):
    """Representation of a switch to control the display."""

    def __init__(self, url):
        self._name = "Display Control"
        self._is_on = False
        self._url = url

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self, **kwargs):
        """Send a request to turn on the display."""
        response = requests.get(f"{self._url}/turn_on_display")
        if response.status_code == 200:
            self._is_on = True

    def turn_off(self, **kwargs):
        """Send a request to turn off the display."""
        response = requests.get(f"{self._url}/turn_off_display")
        if response.status_code == 200:
            self._is_on = False