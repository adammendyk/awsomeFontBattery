"""
FontAwsom icons to be integrated with qtile battery widget to show energy levels
along with orginal widget text.
---
Sample implementation:
    widget.TextBox(
        font="FontAwesome",
        text=afBatteryIcon(1)._get_icon(),
        foreground=colors[5],
        background=colors[1],
        padding=6,
        fontsize=15
    ),
"""

from libqtile import widget
# from pathlib import Path

# Default for battery name
# b_no = 0


class afBatteryIcon:

    # Defaults
    ICONS = {
        "full": "",
        "three-quarters": "",
        "half": "",
        "quarter": "",
        "empty": "",
        "bolt": ""
    }

    _battery = {
        "name": "",
        "icon": "",
        "update": ""
    }

    def _set_battery_name(self):
        self._battery["name"] = "BAT"+(str(self.b_no))

    def _set_battery_icon(self):
        with open(f"/sys/class/power_supply/{self._battery['name']}/capacity") as bat:
            capacity = int(bat.readlines()[0])

        # ranges
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

        # match capacity:
        #     case "full":
        #         status_ico = self.ICONS["full"]
        #     case "three-quarters":
        #         status_ico = self.ICONS["three-quarters"]
        #     case "half":
        #         status_ico = self.ICONS["half"]
        #     case "quarter":
        #         status_ico = self.ICONS["quarter"]
        #     case "empty":
        #         status_ico = self.ICONS["empty"]
        #     case _:
        #         status_ico = self.ICONS["full"]

        self._battery['icon'] = status_ico

    def __init__(self, b_no: int) -> None:
        self.b_no = b_no
        self._set_battery_name()
        self._set_battery_icon()

    def _get_name(self):
        return self._battery['name']

    def _get_icon(self):
        return self._battery['icon']

    def __repr__(self):
        return f"{self._battery['name']}'s current icon is: {self._battery['icon']}"


# if __name__ == "__main__":
#     print(battery_icon(0))
# bt = afBatteryIcon(0)
# print(bt)
# print(bt._get_name())
# print(bt._get_icon())
