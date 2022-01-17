"""
FontAwsom icons to be integrated with qtile battery widget to show energy levels
along with original widget text.
"""

# from libqtile import widget


def BatteryIcon(b_no: int) -> str:
    _BATTERY = "BAT"+(str(b_no))
    with open(f"/sys/class/power_supply/{_BATTERY}/capacity") as BAT:
        capacity = int(BAT.readlines()[0])

    b_icons = {
        "full": "",
        "three-quarters": "",
        "half": "",
        "quarter": "",
        "empty": "",
        "bolt": ""
    }

    # ranges
    battery_ico = 1
    if capacity <= 100:
        battery_ico = b_icons["full"]
    if capacity <= 75:
        battery_ico = b_icons["three-quarters"]
    if capacity <= 50:
        battery_ico = b_icons["half"]
    if capacity <= 25:
        battery_ico = b_icons["quarter"]
    if capacity <= 5:
        battery_ico = b_icons["empty"]

    # match capacity:
    #     case "full":
    #         battery_ico = b_icons["full"]
    #     case "three-quarters":
    #         battery_ico = b_icons["three-quarters"]
    #     case "half":
    #         battery_ico = b_icons["half"]
    #     case "quarter":
    #         battery_ico = b_icons["quarter"]
    #     case "empty":
    #         battery_ico = b_icons["empty"]
    #     case _:
    #         battery_ico = b_icons["full"]

    return battery_ico


if __name__ == "__main__":
    pass

# print(BatteryIcon(0))
