from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatSessionListSerializer
from .curator_service import WhiscuratorService



class ChatSessionListView(generics.ListAPIView):
    # 대화 세션 목록
    serializer_class = ChatSessionListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    

class ChatSessionDetailView(generics.RetrieveAPIView):
    # 대화 세션 상세 (메시지 포함)
    serializer_class = ChatSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    

class ChatSessionDeleteView(generics.DestroyAPIView):
    # 대화 세션 삭제
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)


class SendMessageView(APIView):
    # 메시지 전송 + AI 응답
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        message = request.data.get('message', '').strip()
        session_id = request.data.get('session_id', None)

        if not message:
            return Response(
                {"detail": "메시지를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST
            )    
        
        service = WhiscuratorService()

        # 세션 가져오거나 새로 생성
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id, user=user)
            except ChatSession.DoesNotExist:
                return Response(
                    {"detail": "세션을 찾을 수 없어요."},
                    status=status.HTTP_404_NOT_FOUND
                )
            is_first_message = not session.messages.exists()
        else:
            # 첫 메시지면 세션 + 제목 같이 생성
            title = service.generate_title(message)
            session = ChatSession.objects.create(user=user, title=title)
            is_first_message = True        

        # 유저 메시지 저장
        ChatMessage.objects.create(
            session=session,
            role='user',
            content=message
        )

        # 대화 히스토리 구성 (최근 10개)
        history = list(
            session.messages.order_by('-created_at')[:10]
            .values('role', 'content')
        )
        history.reverse()

        # AI 응답 생성
        ai_response, recommended_whiskies = service.get_ai_response(history, user)

        # AI 메시지 저장
        ai_message = ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=ai_response
        )

        # 추천 위스키 연결
        if recommended_whiskies:
            ai_message.recommended_whiskies.set(recommended_whiskies)
        
        return Response({
            "session_id": session.id,
            "session_title": session.title,
            "is_first_message": is_first_message,
            "user_message": message,
            "ai_response": ai_response,
            "recommended_whiskies": recommended_whiskies,            
        }, status=status.HTTP_200_OK)
    