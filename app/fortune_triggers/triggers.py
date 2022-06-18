from dateutil.easter import easter
from .triggers_base import BaseFortuneTriggers


class FortuneTriggers(BaseFortuneTriggers):
    def trigger_christmas(self, *args, **kwargs):
        return kwargs["day"] in range(24, 27) and kwargs["month"] == 12

    def trigger_halloween(self, *args, **kwargs):
        return kwargs["day"] == 31 and kwargs["month"] == 10

    def trigger_easter(self, *args, **kwargs):
        easter_date = easter(kwargs["year"])
        return easter_date.day == kwargs["day"] and easter_date.month == kwargs["month"]

    def trigger_new_years_eve(self, *args, **kwargs):
        return kwargs["day"] == 31 and kwargs["month"] == 12

    def trigger_new_year(self, *args, **kwargs):
        return kwargs["day"] == 1 and kwargs["month"] == 1

    def trigger_morning(self, *args, **kwargs):
        return kwargs["hour"] in range(6, 13)

    def trigger_noon(self, *args, **kwargs):
        return kwargs["hour"] in range(13, 18)

    def trigger_evening(self, *args, **kwargs):
        return kwargs["hour"] in range(18, 23)

    def trigger_night(self, *args, **kwargs):
        return kwargs["hour"] in range(23, 6)

    def trigger_default(self, *args, **kwargs):
        return True

    order = [
        trigger_christmas,
        trigger_halloween,
        trigger_easter,
        trigger_new_years_eve,
        trigger_new_year,
        trigger_morning,
        trigger_noon,
        trigger_evening,
        trigger_night,
        trigger_default
    ]
