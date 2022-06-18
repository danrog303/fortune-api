from rest_framework import serializers
from fortune_models.models import FortunePool, FortuneEntry, FortuneImage


class FortunePoolRefreshDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FortunePool
        fields = ["last_refresh_date", "next_refresh_date"]


class FortunePoolPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = FortunePool
        fields = ["name", "description"]


class FortuneImagePublicSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='media-display',
        lookup_field='key',
        lookup_url_kwarg="media_key"
    )

    class Meta:
        model = FortuneImage
        fields = ["url"]


class FortuneEntryPublicSerializer(serializers.ModelSerializer):
    pool = FortunePoolRefreshDatesSerializer()
    image = FortuneImagePublicSerializer()

    class Meta:
        model = FortuneEntry
        fields = ["text", "image", "pool"]

    def get_dates(self):
        return FortunePoolRefreshDatesSerializer()
