"""Сенсоры для Sim2M интеграции."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Настройка сенсоров."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        Sim2MBalanceSensor(coordinator, entry),
        Sim2MTrafficLimitSensor(coordinator, entry),
        Sim2MTrafficUsedSensor(coordinator, entry),
        Sim2MTrafficRemainSensor(coordinator, entry),
        Sim2MTrafficPercentSensor(coordinator, entry),
    ]

    async_add_entities(entities)


class Sim2MSensorBase(CoordinatorEntity, SensorEntity):
    """Базовый сенсор Sim2M."""

    def __init__(self, coordinator, entry):
        """Инициализация."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": f"Sim2M {coordinator.data.get('score', 'Unknown')}",
            "manufacturer": "Sim2M",
            "model": coordinator.data.get('simCard', {}).get('operator', 'Unknown'),
        }


class Sim2MBalanceSensor(Sim2MSensorBase):
    """Сенсор баланса."""

    _attr_name = "Баланс"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_native_unit_of_measurement = "₽"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self):
        """Уникальный ID."""
        return f"{self._entry.entry_id}_balance"

    @property
    def native_value(self):
        """Значение."""
        return self.coordinator.data.get("balance", 0)


class Sim2MTrafficLimitSensor(Sim2MSensorBase):
    """Сенсор лимита трафика."""

    _attr_name = "Трафик Лимит"
    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_native_unit_of_measurement = "GB"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self):
        """Уникальный ID."""
        return f"{self._entry.entry_id}_traffic_limit"

    @property
    def native_value(self):
        """Значение в ГБ."""
        traffic = self.coordinator.data.get("traffic", {})
        limit_mb = traffic.get("limit", 0)
        return round(limit_mb / 1024, 2) if limit_mb else 0


class Sim2MTrafficUsedSensor(Sim2MSensorBase):
    """Сенсор использованного трафика."""

    _attr_name = "Трафик Использовано"
    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_native_unit_of_measurement = "GB"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    @property
    def unique_id(self):
        """Уникальный ID."""
        return f"{self._entry.entry_id}_traffic_used"

    @property
    def native_value(self):
        """Значение в ГБ."""
        traffic = self.coordinator.data.get("traffic", {})
        used_mb = traffic.get("used", 0)
        return round(used_mb / 1024, 2) if used_mb else 0


class Sim2MTrafficRemainSensor(Sim2MSensorBase):
    """Сенсор остатка трафика."""

    _attr_name = "Трафик Осталось"
    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_native_unit_of_measurement = "GB"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self):
        """Уникальный ID."""
        return f"{self._entry.entry_id}_traffic_remain"

    @property
    def native_value(self):
        """Значение в ГБ."""
        traffic = self.coordinator.data.get("traffic", {})
        remain_mb = traffic.get("remain", 0)
        return round(remain_mb / 1024, 2) if remain_mb else 0


class Sim2MTrafficPercentSensor(Sim2MSensorBase):
    """Сенсор процента использования трафика."""

    _attr_name = "Трафик Использовано %"
    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def unique_id(self):
        """Уникальный ID."""
        return f"{self._entry.entry_id}_traffic_percent"

    @property
    def native_value(self):
        """Значение в процентах."""
        traffic = self.coordinator.data.get("traffic", {})
        limit = traffic.get("limit", 0)
        used = traffic.get("used", 0)

        if limit > 0:
            return round((used / limit) * 100, 1)
        return 0
