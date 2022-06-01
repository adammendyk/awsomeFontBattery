This is very simple Qtile widget to compelement/replace built one.
It displays Font Awsome battery icon symbols based on the battery capacity levels.

Widget or link to it must be in the same directory as Qtile config file and must be imported as usual:
from awsomefont_battery_icon import afBatteryIcon

Battery name is set to BAT0 by default. To change it add:
widget.afBatteryIcon(
battery="BAT#"
).
"#" - being number of battery you want to add (0, 1, 2...)

Editable parameters are:
-> battery = "BAT0"
"System battery name (BAT0, BAT1, BAT2...)"
-> update_interval = 30
"Update interval seconds."
-> alert = 9
"Alert battery level. x out of 100%"
-> foreground = "#f3f4f5"
"Icon colour"
-> alert_color = "#cd1f3f"
"Icon olour when empty."
plus normal widget parameters as background and such...

Plugin/widget is free and may be edited freely.
