from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import TastingNote
from .serializers import TastingNoteSerializer, TastingNoteCreateUpdateSerializer



class TastingNoteListView(generics.ListAPIView):
    # 둘러보기 = 공개 노트 전체 피드
    serializer_class = TastingNoteSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['whisky__country', 'whisky__whisky_type', 'whisky__region']
    search_fields = ['whisky__name', 'whisky__distillery', 'tags']
    ordering_fields = ['tasted_at', 'rating', 'created_at']
    ordering = ['-tasted_at']

    def get_queryset(self):
        queryset = TastingNote.objects.filter(
            is_public=True
        ).select_related('user', 'whisky')

        # 특정 유저 노트만 보기
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        
        # 특정 위스키 노트만 보기
        whisky_id = self.request.query_params.get('whisky_id')
        if whisky_id:
            queryset = queryset.filter(whisky__id=whisky_id)

        return queryset


class MyTastingNoteListView(generics.ListAPIView):
    # 내 기록 - 내 노트 전체 (비공개 포함)
    serializer_class = TastingNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['tasted_at', 'rating', 'created_at']
    ordering = ['-tasted_at']

    def get_queryset(self):
        return TastingNote.objects.filter(
            user=self.request.user
        ).select_related('whisky')


class TastingNoteCreateView(generics.CreateAPIView):
    # 테이스팅 노트 작성
    serializer_class = TastingNoteCreateUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class TastingNoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    # 테이스팅 노트 상세 조회 / 수정 / 삭제
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return TastingNoteCreateUpdateSerializer
        return TastingNoteSerializer
    
    def get_queryset(self):
        return TastingNote.objects.select_related('user', 'whisky')

    def get_object(self):
        obj = super().get_object()
        # 비공개 노트는 작성자만 조회 가능
        if not obj.is_public and obj.user != self.request.user:
            raise PermissionDenied("비공개 노트예요.")
        return obj
    
    def perform_update(self, serializer):
        # 수정은 작성자만 가능
        if self.get_object().user != self.request.user:
            raise PermissionDenied("본인 노트만 수정할 수 있어요.")
        serializer.save()

    def perform_destroy(self, instance):
        # 삭제는 작성자만 가능
        if instance.user != self.request.user:
            raise PermissionDenied("본인 노트만 삭제할 수 있어요.")
        instance.delete()
    
    