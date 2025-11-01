"""Config flow для Sim2M интеграции."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from .api import Sim2MAPI

import logging
_LOGGER = logging.getLogger(__name__)


class Sim2MConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow для Sim2M."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Обработка пользовательского ввода."""
        errors = {}

        if user_input is not None:
            refresh_token = user_input["refresh_token"]
            account_id = user_input["account_id"]

            # Проверяем токен
            api = Sim2MAPI(refresh_token)

            try:
                data = await self.hass.async_add_executor_job(api.get_data, account_id)

                if data:
                    # Создаем unique_id из номера счета
                    await self.async_set_unique_id(f"sim2m_{data['score']}")
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title=f"Sim2M {data['score']}",
                        data=user_input,
                    )
                else:
                    errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Ошибка проверки токена")
                errors["base"] = "unknown"

        # Показываем форму
        data_schema = vol.Schema({
            vol.Required("refresh_token"): str,
            vol.Required("account_id", default="95143"): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
