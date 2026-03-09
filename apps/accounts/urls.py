from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.ProfileView.as_view(), name='profile'),
    path('me/delete/', views.DeleteAccountView.as_view(), name='delete_account'),
    path('me/password/', views.PasswordChangeView.as_view(), name='password_change'),
    path('me/mypage/', views.MyPageView.as_view(), name='mypage'),
    path('me/journey/', views.MyJourneyView.as_view(), name='journey'),
]
