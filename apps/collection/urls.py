from django.urls import path
from . import views

urlpatterns = [
    # 장식장
    path('', views.CollecctionListView.as_view(), name='collection-list'),
    path('<int:whisky_id>/add/', views.CollectionAddView.as_view(), name='collection-add'),
    path('<int:whisky_id>/remove/', views.CollectionRemoveView.as_view(), name='collection-remove'),

    # 위시리스트
    path('wishlist/', views.WishlistListView.as_view(), name='wishlist-list'),
    path('wishlist/<int:whisky_id>/add/', views.WishlistAddView.as_view(), name='wishlist-add'),
    path('wishlist/<int:whisky_id>/remove/', views.WishlistRemoveView.as_view(), name='wishlist-remove'),
]