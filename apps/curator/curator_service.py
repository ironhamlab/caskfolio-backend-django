from django.conf import settings
from openai import OpenAI
from apps.whisky.models import Whisky

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class WhiscuratorService:

    SYSTEM_PROMPT = """
    당신은 Caskfolio의 AI 위스키 큐레이터 'Whiscurator'입니다.
    위스키 전문 지식을 바탕으로 유저의 취향과 상황에 맞는 위스키를 추천하고,
    위스키에 대한 궁금증을 친절하게 답변해주세요.

    답변 규칙:
    1. 친근하고 전문적인 톤으로 답변하세요.
    2. 위스키 추천 시 반드시 추천 이유를 함께 설명하세요.
    3. 추천하는 위스키는 반드시 아래 제공된 위스키 DB에 있는 것만 추천하세요.
    4. 서빙 방식(니트/온더락/하이볼 등)도 함께 안내해주세요.
    5. 답변은 한국어로 해주세요.
    6. 추천 위스키가 있으면 답변 마지막에 반드시 아래 형식으로 추가하세요.
    [RECOMMEND]위스키명1,위스키명2[/RECOMMEND]
    """


    def get_whisky_context(self):
        # RAG용 위스키 DB 컨텍스트 생성
        whiskies = Whisky.objects.prefetch_related('cask_types').all()
        context = []
        for w in whiskies:
            casks = ', '.join([c.name for c in w.cask_types.all()])
            context.append(
                f"위스키명: {w.name} | 증류소: {w.distillery} | "
                f"국가: {w.country} | 스타일: {w.whisky_type} | "
                f"지역: {w.region} | 피트강도: {w.peat_level} | "
                f"캐스크: {casks} | 가격대: {w.price_tier} | "
                f"설명: {w.description} | "
                f"테이스팅노트: {w.bartender_tip}"
            )
        return "\n".join(context)
    
    def get_user_context(self, user):
        # 유저 취향 컨텍스트 생성
        from apps.tasting.models import TastingNote
        from apps.collection.models import Collection

        notes = TastingNote.objects.filter(
            user=user
        ).select_related('whisky').order_by('-tasted_at')[:10]

        collections = Collection.objects.filter(
            user=user
        ).select_related('whisky')[:5]

        user_context = []

        if notes.exists():
            liked = [n.whisky.name for n in notes if n.rating >= 4.0]
            disliked = [n.whisky.name for n in notes if n.rating <= 2.0]
            if liked:
                user_context.append(f"높은 별점을 준 위스키: {', '.join(liked)}")
            if disliked:
                user_context.append(f"낮은 별점을 준 위스키: {', '.join(disliked)}")
        
        if collections.exists():
            collected = [c.whisky.name for c in collections]
            user_context.append(f"장식장에 있는 위스키: {', '.join(collected)}")
        
        return "\n".join(user_context) if user_context else "아직 취향 데이터가 없습니다."
    
    def generate_title(self, first_message):
        # 첫 메시지로 세션 제목 생성
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": f"다음 메시지를 20자 이내로 간결하게 요약해줘. 요약문만 출력해: {first_message}"                    
                    }
                ],
                max_tokens=50,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            # API 실패 시 첫 메시지 잘라서 사용
            return first_message[:20] + "..." if len(first_message) > 20 else first_message
    
    def get_ai_response(self, messages, user):
        # AI 응답 생성 (RAG + OpenAI)
        whisky_context = self.get_whisky_context()
        user_context = self.get_user_context(user)

        # 시스템 프롬프트 + 컨텍스트 구성
        system_content = (
            f"{self.SYSTEM_PROMPT}\n\n"
            f"=== 위스키 DB ===\n{whisky_context}\n\n"
            f"=== 유저 취향 정보 ===\n{user_context}"
        )

        # OpenAI messages 형식으로 변환
        openai_messages = [
            {"role": "system", "content": system_content}
        ] + messages

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=openai_messages,
                max_tokens=1000,
                temperature=0.7,
            )
            ai_text = response.choices[0].message.content.strip()

            # 추천 위스키 파싱
            recommended_whiskies = self._parse_recommended_whiskies(ai_text)

            # [RECOMMEND] 태그 제거한 텍스트
            clean_text = ai_text.split('RECOMMEND')[0].strip()

            return clean_text, recommended_whiskies
        
        except Exception as e:
            return f"죄송해요, 일시적인 오류가 발생했어요. 다시 시도해주세요. ({str(e)})", []

    def _parser_recommended_whiskies(self, ai_text):
        # AI 응답에서 추천 위스키 파싱
        try:
            if '[RECOMMEND]' not in ai_text:
                return []
            
            recommend_section = ai_text.split('[RECOMMEND]')[1].split('[/RECOMMEND]')[0]
            whisky_names = [name.strip() for name in recommend_section.split(',')]

            # DB에서 실제 위스키 객체 찾기
            whiskies = []
            for name in whisky_names:
                try:
                    whisky = Whisky.objects.get(name__iexact=name)
                    whiskies.append(whisky)
                except Whisky.DoesNotExist:
                    continue
            return whiskies

        except Exception:
            return [] 