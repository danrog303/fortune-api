from rest_framework.permissions import BasePermission
from fortune_api import finders
from fortune_models.models import FortunePool


class ImageAccessPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        for pool in FortunePool.objects.all():
            applicable_entry = finders.find_applicable_entry(pool)

            if not applicable_entry:
                continue

            if applicable_entry.image.key == obj.key:
                return True

        return False
