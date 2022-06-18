from django.http import HttpResponse
from rest_framework import generics, mixins
from rest_framework.response import Response
from fortune_api.permissions import ImageAccessPermission
from fortune_models.serializers import FortunePoolPublicSerializer, FortuneEntryPublicSerializer
from fortune_models.serializers import FortuneImagePublicSerializer
from fortune_models.models import FortuneEntry, FortunePool, FortuneImage
from fortune_api.finders import find_applicable_entry
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404


class ListFortunePoolsView(generics.ListAPIView):
    queryset = FortunePool.objects.filter(public=True)
    serializer_class = FortunePoolPublicSerializer


class FortuneImageView(generics.RetrieveAPIView):
    queryset = FortuneImage.objects.all()
    serializer_class = FortuneImagePublicSerializer
    permission_classes = [ImageAccessPermission]
    lookup_url_kwarg = "media_key"
    lookup_field = "key"

    def get(self, request, *args, **kwargs):
        obj: FortuneImage = self.get_object()
        return HttpResponse(obj.img.open(), content_type="image/jpeg")


class FortuneEntryView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        applicable_pool = get_object_or_404(FortunePool, name=kwargs.get("pool_name"))
        applicable_entry = find_applicable_entry(applicable_pool)

        if not applicable_entry:
            raise NotFound(detail="Did not found matching fortune entry", code=404)

        data = FortuneEntryPublicSerializer(applicable_entry, context=self.get_serializer_context()).data
        return Response(data)

