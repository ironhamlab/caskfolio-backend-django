from django.urls import path
from . import views

urlpatterns = [
    path('', views.TastingNoteListView.as_view(), name='tasting-list'),
    path('create/', views.TastingNoteCreateView.as_view(), name='tasting-create'),
    path('my/', views.MyTastingNoteListView.as_view(), name='my-tasting-list'),
    path('<int:pk>/', views.TastingNoteDetailView.as_view(), name='tasting-detail'),
]
