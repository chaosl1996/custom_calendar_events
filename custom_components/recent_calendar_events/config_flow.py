from homeassistant import config_entries
import voluptuous as vol

class RecentCalendarEventsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """配置流实现"""

    async def async_step_user(self, user_input=None):
        # 获取所有日历实体
        calendar_entities = [
            entity_id for entity_id in self.hass.states.entity_ids("calendar")
        ]

        if user_input is not None:
            # 验证并创建配置条目
            return self.async_create_entry(
                title=f"Calendar Events: {user_input['calendar_entity']}",
                data=user_input
            )

        # 显示配置表单
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("calendar_entity"): vol.In(calendar_entities),
                vol.Required("event_count", default=3): vol.All(int, vol.Range(min=1, max=20))
            })
        )
