import uuid
from datetime import datetime
from time import time
from django.core.validators import FileExtensionValidator
from django.db import models
from model_utils import Choices
from fortune_triggers.triggers import FortuneTriggers


class FortunePool(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=512, default="", blank=True)
    entry_expiration_seconds = models.PositiveIntegerField(default=1800)
    public = models.BooleanField(default=True)

    @property
    def last_refresh_date(self):
        last_refresh = int(time()) - int(time()) % self.entry_expiration_seconds
        return datetime.fromtimestamp(last_refresh)

    @property
    def next_refresh_date(self):
        next_refresh = int(time()) - int(time()) % self.entry_expiration_seconds + self.entry_expiration_seconds
        return datetime.fromtimestamp(next_refresh)

    def __str__(self):
        return f"({self.pk}) {self.name}"


class FortuneImage(models.Model):
    key = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    img = models.ImageField(validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg"])])
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=128, default="", blank=True)

    def __str__(self):
        return f"({self.pk}) {self.name}"


class FortuneEntry(models.Model):
    pool = models.ForeignKey(FortunePool, on_delete=models.CASCADE)
    image = models.ForeignKey(FortuneImage, on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    trigger = models.TextField(max_length=64, choices=Choices(*FortuneTriggers().get_possible_triggers()))

    def __str__(self):
        return f"{self.pk} {self.pool.name}: [{self.trigger}] {self.text}"

