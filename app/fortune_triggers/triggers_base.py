from datetime import datetime


class BaseFortuneTriggers:
    order = []

    def get_applicable_triggers(self):
        cur_date = datetime.now()

        trigger_kwargs = {
            "day": cur_date.day,
            "month": cur_date.month,
            "year": cur_date.year,
            "hour": cur_date.hour,
            "minute": cur_date.minute,
            "second": cur_date.second
        }

        return [
            trigger.__name__ for trigger in self.order
            if trigger(self, **trigger_kwargs)
        ]

    def get_possible_triggers(self):
        return [trigger.__name__ for trigger in self.order]

