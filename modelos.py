from datetime import datetime, timedelta


class Alarm:
    _id_counter = 0

    def __init__(self, hour, minute, name="Alarma", active=True):
        Alarm._id_counter += 1
        self.id = Alarm._id_counter
        self.hour = hour
        self.minute = minute
        self.name = name
        self.active = active
        self.ringing = False

    def matches(self, h, m):
        return self.active and self.hour == h and self.minute == m

    def time_str(self):
        return f"{self.hour:02d}:{self.minute:02d}"

    def __str__(self):
        icon = "🔔" if self.active else "🔕"
        return f"{icon} {self.time_str()} — {self.name}"

    def __eq__(self, other):
        if isinstance(other, Alarm):
            return self.id == other.id
        return False


class TimeZone:
    def __init__(self, city, country, offset_hours, flag="🌍"):
        self.city = city
        self.country = country
        self.offset_hours = offset_hours
        self.flag = flag

    def get_time(self):
        utc_now = datetime.utcnow()
        return utc_now + timedelta(hours=self.offset_hours)

    def offset_str(self):
        sign = "+" if self.offset_hours >= 0 else ""
        return f"UTC{sign}{self.offset_hours}"

    def __str__(self):
        return f"{self.flag} {self.city}, {self.country} ({self.offset_str()})"


class Lap:
    def __init__(self, number, lap_time, total_time):
        self.number = number
        self.lap_time = lap_time
        self.total_time = total_time

    @staticmethod
    def format_time(seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        hundredths = int((seconds % 1) * 100)
        return f"{mins:02d}:{secs:02d}.{hundredths:02d}"

    def __str__(self):
        return f"Vuelta {self.number:>3d}  │  {self.format_time(self.lap_time)}  │  {self.format_time(self.total_time)}"
