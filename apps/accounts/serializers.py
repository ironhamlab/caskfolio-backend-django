from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # 유저 정보 조회용
    class Meta:
        model = User
        fields = ('id', 'email', 'nickname', 'bio', 'theme', 'note_default_public', 'created_at')
        read_only_fields = ('id', 'email', 'created_at')


class RegisterSerializer(serializers.ModelSerializer):
    # 회원가입용
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'nickname', 'password', 'password2')
    
    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용중인 닉네임이예요.")
        return value
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않아요.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects. create_user(
            email=validated_data['email'],
            username=validated_data['email'],   # username 필드 email로 채움
            nickname=validated_data['nickname'],
            password=validated_data['password'],
        )
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    # 마이페이지 개인정보 수정용
    class Meta:
        model = User
        fields = ('nickname', 'bio', 'theme', 'note_default_public')
    
    def validate_nickname(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임이예요.")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password2 = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 올바르지 않아요.")
        return value
    
    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError("새 비밀번호가 일치하지 않아요.")
        return data
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
