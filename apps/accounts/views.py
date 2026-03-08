from django.shortcuts import render

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, RegisterSerializer, ProfileUpdateSerializer, PasswordChangeSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    # 회원가입
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


class ProfileView(generics.RetrieveUpdateAPIView):
    # 내 프로필 조회 및 수정
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return ProfileUpdateSerializer
        return UserSerializer
    
    def get_object(self):
        return self.request.user
    

class DeleteAccountView(APIView):
    # 회원 탈퇴 (소프트 딜리트)
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        user = request.user
        user.deleted_at = timezone.now()
        user.is_active = False
        user.save()
        return Response({"detail": "탈퇴가 완료됐어요."}, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    # 비밀번호 변경
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "비밀번호가 변경됐어요."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    # 로그아웃 - Refresh 토큰 블랙리스트 처리
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "로그아웃됐어요."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "유효하지 않은 토큰이에요."}, status=status.HTTP_400_BAD_REQUEST)