from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Collection, Wishlist
from .serializers import CollectionSerializer, WishlistSerializer
from apps.whisky.models import Whisky



class CollecctionListView(generics.ListAPIView):
    # 내 장식장 목록
    serializer_class = CollectionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Collection.objects.filter(
            user=self.request.user
        ).select_related('whisky')


class CollectionAddView(APIView):
    # 장식장 추가 - 위시리스트에서 자동 삭제
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, whisky_id):
        whisky = get_object_or_404(Whisky, pk=whisky_id)

        # 이미 장식장에 있는지 확인
        if Collection.objects.filter(user=request.user, whisky=whisky).exists():
            return Response(
                {"detail": "이미 장식장에 있는 위스키예요."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 장식장 추가
        Collection.objects.create(user=request.user, whisky=whisky)

        # 위시리스트에서 자동 삭제
        Wishlist.objects.filter(user=request.user, whisky=whisky).delete()

        return Response(
            {"detail": f"{whisky.name}을(를) 장식장에 추가했어요."},
            status=status.HTTP_201_CREATED
        )


class CollectionRemoveView(APIView):
    # 장식장에서 제거
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, whisky_id):
        collection = get_object_or_404(
            Collection, user=request.user, whisky__id=whisky_id
        )
        collection.delete()
        return Response(
            {"detail": "장식장에서 제거했어요."},
            status=status.HTTP_200_OK
        )
    

class WishlistListView(generics.ListAPIView):
    # 위시리스트 목록
    serializer_class = WishlistSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Wishlist.objects.filter(
            user=self.request.user
        ).select_related('whisky')


class WishlistAddView(APIView):
    # 위시리스트 추가
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, whisky_id):
        whisky = get_object_or_404(Whisky, pk=whisky_id)

        # 이미 장식장에 있으면 위시리스트 추가 불필요
        if Collection.objects.filter(user=request.user, whisky=whisky).exists():
            return Response(
                {"detail": "이미 장식장에 있는 위스키예요. 위시리스트 추가가 필요없어요."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 이미 위시리스트에 있는지 확인
        if Wishlist.objects.filter(user=request.user, whisky=whisky).exists():
            return Response(
                {"detail": "이미 위시리스트에 있는 위스키예요."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        Wishlist.objects.create(user=request.user, whisky=whisky)
        return Response(
            {"detail": f"{whisky.name}을(를) 위시리스트에 추가했어요."},
            status=status.HTTP_201_CREATED
        )
    

class WishlistRemoveView(APIView):
    # 위시리스트에서 제거
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, whisky_id):
        wishlist = get_object_or_404(
            Wishlist, user=request.user, whisky__id=whisky_id
            )
        wishlist.delete()
        return Response(
            {"detail": "위시리스트에서 제거했어요."},
            status=status.HTTP_200_OK
        )