from django.contrib import admin
from .models import FortunePool, FortuneImage, FortuneEntry

admin.site.register(FortunePool)
admin.site.register(FortuneImage)
admin.site.register(FortuneEntry)
