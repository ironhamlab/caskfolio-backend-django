from rest_framework import serializers
from decimal import Decimal
from .models import TastingNote
from apps.whisky.serializers import WhiskyListSerializer


class TastingNoteSerializer(serializers.ModelSerializer):
    # 테이스팅 노트 조회용
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    whisky_detail = WhiskyListSerializer(source='whisky', read_only=True)

    class Meta:
        model = TastingNote
        fields = (
            'id', 'user_nickname', 'whisky', 'whisky_detail',
            'tags', 'note', 'rating', 'is_public',
            'tasted_at', 'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'user_nickname', 'whisky_detail', 'created_at', 'updated_at')


class TastingNoteCreateUpdateSerializer(serializers.ModelSerializer):
    # 테이스팅 노트 작성/수정용

    class Meta:
        model = TastingNote
        fields = ('whisky', 'tags', 'note', 'rating', 'is_public', 'tasted_at')
    
    def validate_rating(self, value):
        if value % Decimal('0.5') != 0:
            raise serializers.ValidationError("별점은 0.5 단위로 입력해주세요.")
        return value
    
    def validate_tags(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("태그는 최대 10개까지 입력할 수 있어요.")
        for tag in value:
            if len(tag) > 20:
                raise serializers.ValidationError("태그는 20자 이내로 입력해주세요.")
        return value
    
    def validate_tasted_at(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("미래 날짜는 입력할 수 없어요.")
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)