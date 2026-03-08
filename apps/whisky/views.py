from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Whisky
from .serializers import WhiskyListSerializer, WhiskyDetailSerializer


class WhiskyListView(generics.ListAPIView):
    # 위스키 목록 - 검색/필터/정렬
    serializer_class = WhiskyListSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # 필터링
    filterset_fields = ['country', 'whisky_type', 'region', 'peat_level', 'price_tier']

    # 검색 (이름, 증류소)
    search_fields = ['name', 'distillery']

    # 정렬
    ordering_fields = ['name', 'age', 'abv', 'created_at']
    ordering = ['name']   # 기본 정렬

    def get_queryset(self):
        queryset = Whisky.objects.prefetch_related('cask_types').all()

        # 캐스크 타입 필터링 (ManytoMany라 별도 처리)
        cask_type = self.request.query_params.get('cask_type')
        if cask_type:
            queryset = queryset.filter(cask_types__name__iexact=cask_type)
        
        return queryset


class WhiskyDetailView(generics.RetrieveAPIView):
    # 위스키 상세 - 도슨트 포함
        serializer_class = WhiskyDetailSerializer
        permission_classes = (AllowAny,)
        queryset = Whisky.objects.prefetch_related('cask_types').all()