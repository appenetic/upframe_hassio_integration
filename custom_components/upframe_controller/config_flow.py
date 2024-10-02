import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class DisplayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Display Control."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Create a config entry with the user-provided name and URL
            return self.async_create_entry(title=user_input["name"], data=user_input)

        # Define the schema with both URL and name
        data_schema = vol.Schema({
            vol.Required("name"): str,  # Ask for a name
            vol.Required("url"): str    # Ask for the URL
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema
        )