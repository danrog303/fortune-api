from rest_framework import serializers
from rest_framework.exceptions import NotFound
from fortune_models.models import FortuneImage, FortunePool, FortuneEntry


class FortunePoolAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = FortunePool
        fields = ["name", "description", "entry_expiration_seconds", "public"]


class FortuneImageAdminSerializer(serializers.ModelSerializer):
    key = serializers.UUIDField(read_only=True)
    description = serializers.CharField(max_length=128)
    img = serializers.ImageField(write_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='media-display',
        lookup_field='key',
        lookup_url_kwarg="media_key",
        read_only=True
    )

    class Meta:
        model = FortuneImage
        fields = ['key', "name", 'description', 'img', "url"]

    def create(self, validated_data):
        return FortuneImage.objects.create(**validated_data)


class FortuneEntryAdminSerializer(serializers.ModelSerializer):
    image = FortuneImageAdminSerializer(read_only=True)
    image_name = serializers.CharField(max_length=128, write_only=True)
    pool = FortunePoolAdminSerializer(read_only=True)
    pool_name = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = FortuneEntry
        fields = ["pool", "pool_name", "image", "image_name", "text", "trigger"]

    def create(self, validated_data):
        images = FortuneImage.objects.filter(name__exact=validated_data["image_name"])
        if not images:
            raise NotFound(f"Did not found image with '{validated_data['image_name']}' name.")
        pools = FortunePool.objects.filter(name__exact=validated_data["pool_name"])
        if not pools:
            raise NotFound(f"Did not found pool with '{validated_data['pool_name']}' name.")
        return FortuneEntry.objects.create(pool=pools.first(),
                                           image=images.first(),
                                           text=validated_data["text"],
                                           trigger=validated_data["trigger"])
