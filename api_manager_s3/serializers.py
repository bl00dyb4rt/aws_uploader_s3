from rest_framework import serializers

from api_manager_s3.models import Images


class ImagesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    full_path = serializers.CharField(required=True, allow_blank=False, max_length=200)
    hash_name = serializers.CharField(required=True, allow_blank=False, max_length=200)

    def create(self, validated_data):
        return Images.objects.create(**validated_data)


class ImagePostSerializer(serializers.Serializer):
    file = serializers.ImageField(max_length=None, allow_empty_file=False)
