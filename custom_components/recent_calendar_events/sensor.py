from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util
from datetime import timedelta
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """配置条目初始化"""
    coordinator = RecentCalendarEventsCoordinator(hass, config_entry.data)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        RecentCalendarEventSensor(coordinator, idx)
        for idx in range(config_entry.data["event_count"])
    ])

class RecentCalendarEventsCoordinator(DataUpdateCoordinator):
    """数据更新协调器"""
    def __init__(self, hass, config):
        super().__init__(
            hass,
            _LOGGER,
            name="Recent Calendar Events",
            update_interval=timedelta(minutes=1)
        )
        self.calendar_entity = config["calendar_entity"]
        self.event_count = config["event_count"]
        self.events = []

    async def _async_update_data(self):
        """获取最新事件"""
        now = dt_util.now()
        end = now + timedelta(days=365)
        events = await self.hass.services.async_call(
            "calendar",
            "async_get_events",
            {
                "entity_id": self.calendar_entity,
                "start_date_time": now,
                "end_date_time": end
            },
            blocking=True,
            return_response=True
        )
        sorted_events = sorted(events, key=lambda e: e["start"])
        self.events = sorted_events[:self.event_count]

class RecentCalendarEventSensor(Entity):
    """单个事件传感器"""
    def __init__(self, coordinator, index):
        self.coordinator = coordinator
        self.index = index
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_event_{index}"
        self._attr_name = f"Recent Event {index + 1}"

    @property
    def state(self):
        """返回事件状态（标题）"""
        if self.index < len(self.coordinator.events):
            return self.coordinator.events[self.index].get("summary", "No Title")
        return "No Event"

    @property
    def extra_state_attributes(self):
        """返回事件详细属性"""
        if self.index >= len(self.coordinator.events):
            return {}
        event = self.coordinator.events[self.index]
        return {
            "start_time": event["start"],
            "end_time": event["end"],
            "description": event.get("description", ""),
            "location": event.get("location", "")
        }

    async def async_update(self):
        """更新数据"""
        await self.coordinator.async_request_refresh()
