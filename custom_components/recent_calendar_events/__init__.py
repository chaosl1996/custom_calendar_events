"""Custom component to display recent calendar events."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "recent_calendar_events"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """初始化集成（无需在此处操作，配置通过 Config Flow 完成）"""
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry):
    """通过配置条目加载集成"""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry):
    """卸载集成时清理资源"""
    await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    return True
