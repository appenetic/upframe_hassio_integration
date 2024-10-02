from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
import aiohttp
import async_timeout
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
    
    @property
    def icon(self):
        return "mdi:monitor-vertical"

    async def async_update(self):
        """Fetch the display status from the server asynchronously."""
        try:
            async with aiohttp.ClientSession() as session:
                async with async_timeout.timeout(10):  # Set a timeout for the request
                    async with session.get(f"{self._url}/system/display_status") as response:
                        if response.status == 200:
                            data = await response.json()
                            self._state = data.get("display_on")
                        else:
                            self._state = None
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            self._state = None