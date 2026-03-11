from django.urls import path
from . import views

urlpatterns = [
    path('sessions/', views.ChatSessionListView.as_view(), name='chat-session-list'),
    path('sessions/<int:pk>/', views.ChatSessionDetailView.as_view(), name='chat-session-detail'),
    path('sessions/<int:pk>/delete/', views.ChatSessionDeleteView.as_view(), name='chat-session-delete'),
    path('chat/', views.SendMessageView.as_view(), name='send-message'),    
]
