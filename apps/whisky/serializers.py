from rest_framework import serializers
from .models import Whisky, CaskType


class CaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaskType
        fields = ('id', 'name', 'description')


class WhiskyListSerializer(serializers.ModelSerializer):
    # 목록용 - 가벼운 정보만
    cask_types = CaskTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Whisky
        fields = (
            'id', 'name', 'distillery', 'country', 'whisky_type',
            'region', 'age', 'abv', 'peat_level', 'price_tier',
            'cask_types', 'flavor_profile', 'image',
        )


class WhiskyDetailSerializer(serializers.ModelSerializer):
    # 상세용 - 도슨트 포함 전체 정보
    cask_types = CaskTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Whisky
        fields = (
            'id', 'name', 'distillery', 'country', 'whisky_type',
            'region', 'age', 'abv', 'peat_level', 'price_tier',
            'cask_types', 'flavor_profile', 'image',
            'description', 'history', 'bartender_tip',
            'pairing', 'serving_guide', 'created_at',
        )