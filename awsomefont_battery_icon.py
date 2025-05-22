"""
A Qtile widget that displays battery status using Font Awesome icons.

This widget shows different icons based on battery capacity and charging status.
It aims to minimize file I/O by reading battery status only during polling
and using instance variables for capacity and status in other methods.

Configuration:
    battery: Name of the battery to monitor (e.g., "BAT0", "BAT1").
             Default: "BAT0"
    update_interval: How often to update the battery status in seconds.
                     Default: 30
    alert: Battery capacity (percentage) at which to change the icon color
           to `alert_color`. Default: 9
    font: Font to use for icons. Default: "FontAwesome"
    foreground: Default color for the icon.
    alert_color: Color for the icon when battery capacity is at or below `alert`.
"""

from libqtile.widget import base


class afBatteryIcon(base.ThreadPoolText):
    """
    A battery widget using Font Awesome icons to display charge levels and status.
    It periodically polls the system for battery capacity and charging status,
    updating the displayed icon and color accordingly.
    """

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
            9,
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
            "Icon color"
        ),
        (
            "alert_color",
            "#cd1f3f",
            "Color when empty."
        )
    ]

    def __init__(self, **config):
        """
        Initializes the widget.
        Sets up default configurations, and performs an initial read of
        battery capacity and status, then sets the initial icon.
        """
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(afBatteryIcon.defaults)
        # Initialize capacity and status from system files
        self.capacity = self._get_battery_capacity()
        self.status = self._get_battery_status()
        # Set the initial icon based on the fetched capacity and status
        self.icon = self.set_icon()

    def _get_battery_capacity(self):
        """Reads battery capacity from /sys/class/power_supply/{battery_name}/capacity."""
        with open(f"/sys/class/power_supply/{self.battery}/capacity") as bat:
            return int((bat.readlines())[0].strip())

    def _get_battery_status(self):
        """Reads battery status from /sys/class/power_supply/{battery_name}/status."""
        with open(f"/sys/class/power_supply/{self.battery}/status") as bat:
            return (bat.readlines())[0].strip()

    def set_icon(self):
        """
        Determines and sets the appropriate battery icon based on current
        `self.status` (e.g., "Charging") and `self.capacity` (percentage).
        The icon is updated in `self.icon` and also returned.
        Relies on `self.capacity` and `self.status` being up-to-date.
        """
        # Icon definitions
        ICONS = {
            "full": "",
            "three-quarters": "",
            "half": "",
            "quarter": "",
            "empty": "",
            "charging": ""  # Bolt icon for charging
        }

        status_ico = ICONS["empty"] # Default to empty if no other conditions match

        # Charging status takes precedence over capacity icons
        if self.status == "Charging":
            status_ico = ICONS["charging"]
        # Set icon based on capacity, from lowest to highest
        elif self.capacity <= 5:  # Very low battery
            status_ico = ICONS["empty"]
        elif self.capacity <= 25: # Low battery
            status_ico = ICONS["quarter"]
        elif self.capacity <= 50: # Half battery
            status_ico = ICONS["half"]
        elif self.capacity <= 75: # Good battery level
            status_ico = ICONS["three-quarters"]
        elif self.capacity <= 100: # Full or near full
            status_ico = ICONS["full"]
        # Note: self.capacity should ideally always fall within 0-100.
        # Consider adding error handling or logging if capacity is out of expected range.

        self.icon = status_ico  # Update the instance's icon attribute
        return status_ico       # Return the determined icon string

    def draw(self):
        """
        Draws the widget.
        Sets the icon color based on `self.capacity` relative to `self.alert`.
        Relies on `self.capacity` being up-to-date from the `poll` method.
        """
        if self.capacity <= self.alert: # Use instance capacity
            self.layout.colour = self.alert_color
        else:
            self.layout.colour = self.foreground
        return base.ThreadPoolText.draw(self)

    def poll(self):
        """
        Called periodically to update battery status and icon.
        1. Fetches the current battery capacity and status from system files.
        2. Updates `self.capacity` and `self.status`.
        3. Calls `self.set_icon()` to update `self.icon` based on the new status.
        4. Returns the new icon text for display.
        """
        # Update instance variables with current battery state
        self.capacity = self._get_battery_capacity()
        self.status = self._get_battery_status()
        
        # Determine and set the new icon based on updated capacity and status
        icon = self.set_icon() # This also updates self.icon
        return icon

    # def __repr__(self):
    #     return f"{self.capacity} = {self.icon}"


# bt = afBatteryIcon(battery="BAT0")
# print(bt.poll())
# print(bt.capacity)
# print(bt.status)
# print(bt.icon)
