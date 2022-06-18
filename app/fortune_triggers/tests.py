from unittest import TestCase
from freezegun import freeze_time
from fortune_triggers.triggers import FortuneTriggers


class TriggersTestCase(TestCase):

    def setUp(self):
        self.triggers = FortuneTriggers()

    @freeze_time("2021-12-25")
    def test_christmas_trigger_should_be_on(self):
        self.assertIn("trigger_christmas", self.triggers.get_applicable_triggers())

    @freeze_time("2021-10-31")
    def test_christmas_trigger_should_be_off(self):
        self.assertNotIn("trigger_christmas", self.triggers.get_applicable_triggers())

    @freeze_time("2012-10-31")
    def test_halloween_trigger_should_be_on(self):
        self.assertIn("trigger_halloween", self.triggers.get_applicable_triggers())

    @freeze_time("2012-01-01")
    def test_halloween_trigger_should_be_off(self):
        self.assertNotIn("trigger_halloween", self.triggers.get_applicable_triggers())
