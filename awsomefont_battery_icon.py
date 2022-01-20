"""
FontAwsom icons to be integrated with qtile battery widget to show energy levels
along with orginal widget text.
Battery name is set to BAT0 by default.

"""

from telnetlib import STATUS
from libqtile.widget import base


bat_name: str = "BAT0"
status: str = ""  # From file /sys/class/power_supply/BAT0/status:Charging or Discharging
capacity: int = 0  # From file /sys/class/power_supply/BAT0/capacity
icon: str = ""  # FontAwsom icon therefore string


class afBatteryIcon(base._TextBox):

    # Class defaults
    defaults = [
        (
            "battery_name",
            bat_name,
            "System battery name (BAT0, BAT1, BAT2...)"
        ),
        (
            "battery_status",
            status,
            "Charging status of selected battery."
        ),
        (
            "battery_icon",
            icon,
            "Status icon (full, three-quarters, half, quarer, empty, charging)"
        ),
        (
            "update_delay",
            60,
            "The delay in seconds between updates"
        )
    ]

    # Class constants
    ICONS = {
        "full": "fu",
        "three-quarters": "tq",
        "half": "ha",
        "quarter": "qu",
        "empty": "em",
        "charging": "ch"
    }

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.add_defaults(afBatteryIcon.defaults)
        self.add_defaults(afBatteryIcon.ICONS)

    def _get_battery_capacity(self):
        with open(f"/sys/class/power_supply/{bat_name}/capacity") as bat:
            capacity = int((bat.readlines())[0])
        return capacity

    def _get_battery_status(self):
        with open(f"/sys/class/power_supply/{bat_name}/status") as bat:
            status = (bat.readlines())[0].strip()
        return status

    def set_icon(self):
        # Ranges
        status_ico = "full"
        if capacity <= 100:
            status_ico = self.ICONS["full"]
        if capacity <= 75:
            status_ico = self.ICONS["three-quarters"]
        if capacity <= 50:
            status_ico = self.ICONS["half"]
        if capacity <= 25:
            status_ico = self.ICONS["quarter"]
        if capacity <= 5:
            status_ico = self.ICONS["empty"]
        if status == "Charging":
            status_ico = self.ICONS["charging"]
        return status_ico

    def poll(self):
        pass


# if __name__ == "__main__":
#     print(battery_icon(0))
bt = afBatteryIcon()
print(bt.defaults)
print(bt._get_battery_capacity())
print(bt._get_battery_status())
print(bt.set_icon())
