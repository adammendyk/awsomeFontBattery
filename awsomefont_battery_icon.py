"""
FontAwsome icons to be integrated with qtile battery widget to show energy levels
along with orginal widget text.
Battery name is set to BAT0 by default. To change it add:
widget.afBatteryIcon(
    battery="BAT#"
)
# - being number of battery you want to add (0, 1, 2...)

"""

from time import sleep
from libqtile.widget import base
# from time import sleep


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
            30,
            "Update interval seconds."
        )
    ]

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(afBatteryIcon.defaults)
        self._get_battery_capacity()
        self._get_battery_status()

    def _get_battery_capacity(self):
        with open(f"/sys/class/power_supply/{self.battery}/capacity") as bat:
            self.capacity = int((bat.readlines())[0])

    def _get_battery_status(self):
        with open(f"/sys/class/power_supply/{self.battery}/status") as bat:
            self.status = (bat.readlines())[0].strip()

    def set_icon(self):
        self._get_battery_capacity()
        self._get_battery_status()
        sleep(1)
        capacity = self.capacity
        status = self.status

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
        status_ico = self.status
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
        if status == "Charging":
            status_ico = ICONS["charging"]
        self.icon = status_ico

    def poll(self):
        self.set_icon()
        # sleep(1)
        return self.icon

    # def __repr__(self):
    #     return f"{self.capacity} = {self.icon}"


bt = afBatteryIcon(battery="BAT0")
print(bt.poll())
print(bt.capacity)
print(bt.status)
print(bt.icon)
