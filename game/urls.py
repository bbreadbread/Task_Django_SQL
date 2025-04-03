from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', views.game_view, name='game'),
    path('privacy/', views.privacy, name='privacy'),
]