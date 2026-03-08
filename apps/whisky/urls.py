from django.urls import path
from . import views

urlpatterns = [
    path('', views.WhiskyListView.as_view(), name='whisky-list'),
    path('<int:pk>/', views.WhiskyDetailView.as_view(), name='whisky-detail'),
]