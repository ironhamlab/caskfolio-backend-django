from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.accounts.urls')),
    # 소셜 로그인은 나중에 붙일 때 추가
    # path('api/v1/auth/social/', include('allauth.socialaccount.urls')),
    path('api/v1/whiskies/', include('apps.whisky.urls')),
    path('api/v1/tasting-notes/', include('apps.tasting.urls')),
    path('api/v1/collection/', include('apps.collection.urls')),
    path('api/v1/curator/', include('apps.curator.urls')),
]
