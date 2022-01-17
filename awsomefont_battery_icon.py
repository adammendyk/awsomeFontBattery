from libqtile import widget
import os


# bt0 = widget.Battery(
#     battery=0,
# )

# b_percentage = bt0._battery.update_status().percent
# b_no = bt0.battery


def awsome_battery_icon(b_no: int) -> str:
    _batt = widget.Battery(
        battery=b_no
    )
    b_percentage = _batt._battery.update_status().percent

    b_icons = {
        "full": "",
        "three-quarters": "",
        "half": "",
        "quarter": "",
        "empty": "",
        "bolt": ""
    }

    capacity = 1
    # ranges
    if b_percentage <= 1:
        capacity = "full"
    if b_percentage <= 0.75:
        capacity = "three-quarters"
    if b_percentage <= 0.50:
        capacity = "half"
    if b_percentage <= 0.25:
        capacity = "quarter"
    if b_percentage <= 0.05:
        capacity = "empty"

    match capacity:
        case "full":
            battery_ico = b_icons["full"]
        case "three-quarters":
            battery_ico = b_icons["three-quarters"]
        case "half":
            battery_ico = b_icons["half"]
        case "quarter":
            battery_ico = b_icons["quarter"]
        case "empty":
            battery_ico = b_icons["empty"]
        case _:
            battery_ico = b_icons["full"]

    return battery_ico


# if __name__ == "__main__":
#     pass

# print(type(awsome_battery_icon(1)))
