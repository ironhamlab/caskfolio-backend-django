from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from apps.tasting.models import TastingNote
from apps.collection.models import Collection, Wishlist

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
        


class MyPageView(APIView):
    # 마이페이지 - 프로필 + 통계 요약
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        tasting_count = TastingNote.objects.filter(user=user).count()
        collection_count = Collection.objects.filter(user=user).count()
        wishlist_count = Wishlist.objects.filter(user=user).count()

        data = {
            "profile": UserSerializer(user).data,
            "stats": {
                "tasting_count": tasting_count,
                "collection_count": collection_count,
                "wishlist_count": wishlist_count,
            }
        }
        return Response(data)


class MyJourneyView(APIView):
    # 나의 위싀 여정 시각화 + 인사이트
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        notes = TastingNote.objects.filter(user=user).select_related('whisky').order_by('tasted_at')

        if not notes.exists():
            return Response({"detail": "아직 기록이 없어요. 첫 위스키를 기록해보세요!"})

        # 1. 시간순 위스키 기록
        timeline = [
            {
                "tasted_at": note.tasted_at,
                "whisky_name": note.whisky.name,
                "whisky_type": note.whisky.whisky_type,
                "region": note.whisky.region,
                "country": note.whisky.country,
                "peat_level": note.whisky.peat_level,
                "rating": note.rating,                
            }
            for note in notes
        ]

        # 2. 지역 탐색 통계
        region_stats = (
            notes.values('whisky__region')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # 3. 국가 탐색 통계
        country_stats = (
            notes.values('whisky__country')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # 4. 스타일 탐색 통계
        type_stats = (
            notes.values('whisky__whisky_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # 5. 피트 강도 변화
        peat_order = {"none": 0, "light": 1, "medium": 2, "heavy": 3}
        peat_timeline = [
            {
                "tasted_at": note.tasted_at,
                "peat_level": note.whisky.peat_level,
                "peat_score": peat_order.get(note.whisky.peat_level, 0),
            }
            for note in notes            
        ]

        # 6. 인사이트 생성
        insights = self._generate_insights(notes, type_stats, region_stats)

        return Response({
            "timeline": timeline,
            "region_stats": list(region_stats),
            "country_stats": list(country_stats),
            "type_stats": list(type_stats),
            "peat_timeline": peat_timeline,
            "insights": insights,            
        })

    def _generate_insights(self, notes, type_stats, region_stats):
        insights = []
        total = notes.count()

        # 가장 많이 탐색한 스타일
        if type_stats:
            top_type = type_stats[0]['whisky__whisky_type']
            top_type_count = type_stats[0]['count']
            insights.append(
                f"지금까지 {top_type.replace('_', ' ').title()}을(를) 가장 많이 즐기셨어요. ({top_type_count}번)"
            )

        # 피트 성향
        peat_order = {"none": 0, "light": 1, "medium": 2, "heavy": 3}
        peat_scores = [peat_order.get(n.whisky.peat_level, 0) for n in notes]
        avg_peat = sum(peat_scores) / len(peat_scores)
        if avg_peat >= 2:
            insights.append("피트향이 강한 위스키를 선호하시는 편이에요. 🔥")
        elif avg_peat >= 1:
            insights.append("피트향을 적당히 즐기시는 편이에요.")
        else:
            insights.append("피트향이 없는 부드러운 위스키를 선호하시는 편이에요.")

        # 탐색한 국가 수
        country_count = notes.values('whisky__country').distinct().count()
        if country_count >= 3:
            insights.append(f"{country_count}개 나라의 위스키를 탐험하셨어요! 🌍")
        elif country_count == 2:
            insights.append("두 나라의 위스키를 경험해보셨네요.")
        else:
            insights.append("한 나라의 위스키를 집중 탐구 중이에요.")

        # 총 기록 수
        if total >= 10:
            insights.append(f"벌써 {total}번의 테이스팅을 기록하셨어요. 진정한 위스키 탐험가네요! 🥃")
        elif total >= 5:
            insights.append(f"{total}번의 테이스팅을 기록하셨어요. 위스키의 매력에 빠져들고 있어요!")
        else:
            insights.append(f"{total}번의 테이스팅을 기록하셨어요. 이제 막 시작이에요!")

        # 평균 별점
        avg_rating = notes.aggregate(Avg('rating'))['rating__avg']
        if avg_rating:
            insights.append(f"평균 별점은 {avg_rating:.1f}점이에요.")

        return insights