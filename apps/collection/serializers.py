from rest_framework import serializers
from .models import Collection, Wishlist
from apps.whisky.serializers import WhiskyListSerializer


class CollectionSerializer(serializers.ModelSerializer):
    whisky_detail = WhiskyListSerializer(source='whisky', read_only=True)

    class Meta:
        model = Collection
        fields = ('id', 'whisky', 'whisky_detail', 'added_at')
        read_only_fields = ('id', 'whisky_detail', 'added_at')


class WishlistSerializer(serializers.ModelSerializer):
    whisky_detail = WhiskyListSerializer(source='whisky', read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'whisky', 'whisky_detail', 'added_at')
        read_only_fields = ('id', 'whisky_detail', 'added_at')