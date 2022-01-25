"""
FontAwsome icons integrated with qtile battery widget to show energy levels.
Battery name is set to BAT0 by default. To change it add:
widget.afBatteryIcon(
    battery="BAT#"
)
# - being number of battery you want to add (0, 1, 2...)
"""

from libqtile.widget import base


class afBatteryIcon(base.ThreadPoolText):

    # Class defaults
    defaults = [
        (
            "battery",
            "BAT0",
            "System battery name (BAT0, BAT1, BAT2...)"
        ),
        (
            "status",
            None,
            "Charging status of selected battery."
        ),
        (
            "capacity",
            None,
            "Actual battery capacity in percents."
        ),
        (
            "icon",
            None,
            "Status icon (full, three-quarters, half, quarer, empty, charging)"
        ),
        (
            "update_interval",
            30,
            "Update interval seconds."
        ),
        (
            "alert",
            5,
            "Alert battery level."
        ),
        (
            "font",
            "FontAwsome",
            "FontAwsome is mandatory to properly display icons."
        ),
        (
            "foreground",
            "#f3f4f5",
            "Icon colour"
        ),
        (
            "alert_colour",
            "#cd1f3f",
            "Colour when empty."
        )
    ]

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(afBatteryIcon.defaults)
        self.capacity = self._get_battery_capacity()
        self.status = self._get_battery_status()
        self.icon = self.set_icon()

    def _get_battery_capacity(self):
        with open(f"/sys/class/power_supply/{self.battery}/capacity") as bat:
            return int((bat.readlines())[0].strip())

    def _get_battery_status(self):
        with open(f"/sys/class/power_supply/{self.battery}/status") as bat:
            return (bat.readlines())[0].strip()

    def set_icon(self):
        current_capacity = self._get_battery_capacity()
        current_status = self._get_battery_status()

        # Function constants
        ICONS = {
            "full": "",
            "three-quarters": "",
            "half": "",
            "quarter": "",
            "empty": "",
            "charging": ""
        }
        # Ranges
        status_ico = ""
        if current_capacity <= 100:
            status_ico = ICONS["full"]
        if current_capacity <= 75:
            status_ico = ICONS["three-quarters"]
        if current_capacity <= 50:
            status_ico = ICONS["half"]
        if current_capacity <= 25:
            status_ico = ICONS["quarter"]
        if current_capacity <= 5:
            status_ico = ICONS["empty"]
        if current_status == "Charging":
            status_ico = ICONS["charging"]
        # self.icon = status_ico
        return status_ico

    def draw(self):
        if self.capacity <= self.alert:
            self.layout.colour = self.alert_colour
        else:
            self.layout.colour = self.foreground
        base.ThreadPoolText.draw(self)

    def poll(self):
        icon = self.set_icon()
        return icon

    # def __repr__(self):
    #     return f"{self.capacity} = {self.icon}"


# bt = afBatteryIcon(battery="BAT0")
# print(bt.poll())
# print(bt.capacity)
# print(bt.status)
# print(bt.icon)
