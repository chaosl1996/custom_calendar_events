class RecentCalendarEventSensor(Entity):
    def __init__(self, coordinator, index):
        self.coordinator = coordinator
        self.index = index
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_event_{index}"
        self._attr_name = f"Recent Event {index + 1}"
        self._attr_icon = "mdi:calendar"  # 新增图标属性

    @property
    def should_poll(self):
        """禁用轮询，使用 Coordinator 更新"""
        return False
