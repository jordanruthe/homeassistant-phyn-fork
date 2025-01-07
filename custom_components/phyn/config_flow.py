"""Config flow for phyn integration."""
from aiophyn import async_get_api
from aiophyn.errors import RequestError
from botocore.exceptions import ClientError
import voluptuous as vol

from homeassistant import config_entries, core, exceptions
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, LOGGER

BRANDS = ["Phyn", "Kohler"]

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Required("Brand"): vol.In(BRANDS),
})


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    session = async_get_clientsession(hass)
    try:
        api = await async_get_api(
            data[CONF_USERNAME], data[CONF_PASSWORD], phyn_brand=data["Brand"].lower(), session=session
        )
    except RequestError as request_error:
        LOGGER.error("Error connecting to the Phyn API: %s", request_error)
        raise CannotConnect from request_error

    homes = await api.home.get_homes(data[CONF_USERNAME])
    return {"title": homes[0]["alias_name"]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for phyn."""

    VERSION = 1
    MINOR_VERSION = 2

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_USERNAME])
            self._abort_if_unique_id_configured()
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except ClientError as error:
                if error.response['Error']['Code'] == "NotAuthorizedException":
                    errors["base"] = "invalid_auth"
                else:
                    errors["base"] = "cannot_connect"
            except CannotConnect:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
    
    async def async_step_reconfigure(self, user_input: dict[str, any] | None = None):
        errors = {}
        reconfigure_entry = self._get_reconfigure_entry()
        LOGGER.debug("Reconfigure entry: %s" % reconfigure_entry)
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_update_reload_and_abort(
                    reconfigure_entry, data_updates={
                        CONF_USERNAME: user_input[CONF_USERNAME],
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                        "Brand": user_input["Brand"]
                    }
                )
                return self.async_create_entry(title=info["title"], data=user_input)
            except ClientError as error:
                if error.response['Error']['Code'] == "NotAuthorizedException":
                    errors["base"] = "invalid_auth"
                else:
                    errors["base"] = "cannot_connect"
            except CannotConnect:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=DATA_SCHEMA,
            errors=errors
        )

class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
