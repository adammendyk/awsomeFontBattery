"""
FontAwsom icons to be integrated with qtile battery widget to show energy levels
along with orginal widget text.
"""

from libqtile import widget
from pathlib import Path

# Default for battery name
b_no = 0


class BatteryIcon:

    _BATTERY = {
        "name": "BAT0",
        "icon": "fu"
    }

    def __init__(self, b_no: int) -> None:
        self.b_no = b_no

    def bat_name(self, b_no):
        self._BATTERY["name"] = "BAT"+(str(b_no))

    # Defaults
    b_icons = {
        "full": "fu",
        "three-quarters": "tq",
        "half": "ha",
        "quarter": "qu",
        "empty": "em",
        "bolt": "bt"
    }

    def battery_icon(self):
        with open(f"/sys/class/power_supply/{_BATTERY['name']}/capacity") as bat:
            capacity = int(bat.readlines()[0])

        # ranges
        status_ico = 1
        if capacity <= 100:
            status_ico = b_icons["full"]
        if capacity <= 75:
            status_ico = b_icons["three-quarters"]
        if capacity <= 50:
            status_ico = b_icons["half"]
        if capacity <= 25:
            status_ico = b_icons["quarter"]
        if capacity <= 5:
            status_ico = b_icons["empty"]

        # match capacity:
        #     case "full":
        #         status_ico = b_icons["full"]
        #     case "three-quarters":
        #         status_ico = b_icons["three-quarters"]
        #     case "half":
        #         status_ico = b_icons["half"]
        #     case "quarter":
        #         status_ico = b_icons["quarter"]
        #     case "empty":
        #         status_ico = b_icons["empty"]
        #     case _:
        #         status_ico = b_icons["full"]

        self._BATTERY['icon'] = status_ico

    def _get_name(self):
        return self._BATTERY['name']

    def _get_icon(self):
        return self._BATTERY['icon']

    def __repr__(self):
        return f"{self._BATTERY['name']}'s current icon is: {self._BATTERY['icon']}"


# if __name__ == "__main__":
#     print(battery_icon(0))
bt0 = BatteryIcon(0)
# print(bt0)
print(bt0._get_name())
print(bt0._get_icon())
