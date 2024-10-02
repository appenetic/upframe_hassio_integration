import aiohttp
import async_timeout
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

    @property
    def icon(self):
        """Return the icon to be used for this entity."""
        return "mdi:monitor-vertical"

    async def async_update(self):
        """Fetch the display status to sync the switch state."""
        try:
            async with aiohttp.ClientSession() as session:
                async with async_timeout.timeout(10):  # Timeout of 10 seconds
                    async with session.get(f"{self._url}/system/display_status") as response:
                        if response.status == 200:
                            data = await response.json()
                            is_display_on = data.get("display_on")
                            self._is_on = True if is_display_on else False
        except (aiohttp.ClientError, asyncio.TimeoutError):
            self._is_on = False

    async def async_turn_on(self, **kwargs):
        """Send a request to turn on the display."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._url}/system/turn_on_display") as response:
                if response.status == 200:
                    self._is_on = True

    async def async_turn_off(self, **kwargs):
        """Send a request to turn off the display."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._url}/system/turn_off_display") as response:
                if response.status == 200:
                    self._is_on = False