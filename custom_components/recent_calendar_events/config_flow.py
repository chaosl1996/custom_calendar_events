from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

class RecentCalendarEventsConfigFlow(config_entries.ConfigFlow, domain="recent_calendar_events"):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Recent Calendar Events", data=user_input)

        # 获取所有日历实体
        calendar_entities = [
            entity_id for entity_id in self.hass.states.entity_ids("calendar")
        ]

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("calendar_entity"): vol.In(calendar_entities),
                vol.Required("event_count", default=3): vol.All(int, vol.Range(min=1, max=20))
            }),
            errors=errors
        )
