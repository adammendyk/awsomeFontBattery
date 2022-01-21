"""
FontAwsome icons to be integrated with qtile battery widget to show energy levels
along with orginal widget text.
Battery name is set to BAT0 by default. To change it add:
widget.afBatteryIcon(
    battery="BAT#"
)
# - being number of battery you want to add (0, 1, 2...)

"""

from libqtile.widget import base


class afBatteryIcon(base._TextBox):

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
            5,
            "Update interval seconds."
        )
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(afBatteryIcon.defaults)
        percent = self._get_battery_capacity()
        self._get_battery_status()
        self.set_icon()

    def _get_battery_capacity(self):
        with open(f"/sys/class/power_supply/{self.battery}/capacity") as bat:
            percent = int((bat.readlines())[0])
        return percent

    def _get_battery_status(self):
        with open(f"/sys/class/power_supply/{self.battery}/status") as bat:
            status = (bat.readlines())[0].strip()
        return status

    def set_icon(self):
        capacity = self._get_battery_capacity()
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
        # status_ico = "full"
        if capacity <= 100:
            status_ico = ICONS["full"]
        if capacity <= 75:
            status_ico = ICONS["three-quarters"]
        if capacity <= 50:
            status_ico = ICONS["half"]
        if capacity <= 25:
            status_ico = ICONS["quarter"]
        if capacity <= 5:
            status_ico = ICONS["empty"]
        if self.status == "Charging":
            status_ico = ICONS["charging"]
        return status_ico

    # def timer_setup(self):

    #     self.timeout_add(self.update_delay, self.timer_setup)

    def poll(self):
        percentage = self._get_battery_capacity()
        icon = percentage.get(self.capacity, [1])
        return icon


# if __name__ == "__main__":
#     print(battery_icon(0))
# bt = afBatteryIcon(battery="BAT0")
# print(bt.defaults)
# print(bt._get_battery_capacity())
# # print(bt._get_battery_status())
# print(bt.set_icon())
