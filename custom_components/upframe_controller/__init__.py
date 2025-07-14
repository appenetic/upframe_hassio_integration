import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the display control component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up display control from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Store config entry
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    # Use the new API method (note the 's' at the end)
    await hass.config_entries.async_forward_entry_setups(entry, ["switch", "sensor"])
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Use the new API method for unloading
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["switch", "sensor"])
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok