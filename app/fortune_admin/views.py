from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from fortune_api.finders import find_applicable_trigger_for_pool
from fortune_models.models import FortunePool, FortuneImage, FortuneEntry
from fortune_triggers.triggers import FortuneTriggers
from fortune_admin.serializers import FortuneImageAdminSerializer, FortunePoolAdminSerializer, \
    FortuneEntryAdminSerializer


class EntryListCreateView(generics.ListCreateAPIView):
    queryset = FortuneEntry.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = FortuneEntryAdminSerializer


class PoolListCreateView(generics.ListCreateAPIView):
    queryset = FortunePool.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = FortunePoolAdminSerializer


class ImageListCreateView(generics.ListCreateAPIView):
    queryset = FortuneImage.objects.all()
    serializer_class = FortuneImageAdminSerializer
    permission_classes = [IsAdminUser]


class ApplicableTriggerView(generics.GenericAPIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        result = {"matches": FortuneTriggers().get_applicable_triggers(), "pools": {}}
        for pool in FortunePool.objects.all():
            result["pools"][pool.name] = find_applicable_trigger_for_pool(pool)
        return Response(result)
