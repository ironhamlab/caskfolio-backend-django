from rest_framework import serializers
from .models import ChatSession, ChatMessage
from apps.whisky.serializers import WhiskyListSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    recommended_whiskies = WhiskyListSerializer(many=True, read_only=True)

    class Meta:
        model = ChatMessage
        fields = ('id', 'role', 'content', 'recommended_whiskies', 'created_at')
        read_only_fields = ('id', 'role', 'recommended_whiskies', 'created_at')


class ChatSessionSerializer(serializers.ModelSerializer):
    message = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ('id', 'title', 'messages', 'created_at')
        read_only_fields = ('id', 'title', 'messages', 'created_at')


class ChatSessionListSerializer(serializers.ModelSerializer):
    # 세션 목록용 - 메시지 제외하고 타이틀만 노출
    class Meta:
        model = ChatSession
        fields = ('id', 'title', 'created_at')