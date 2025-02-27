from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "recent_calendar_events"

async def async_setup_entry(hass: HomeAssistant, config_entry):
    """通过配置条目初始化传感器"""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry):
    """卸载集成"""
    await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    return True
