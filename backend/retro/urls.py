# retro/urls.py
from django.urls import path
from .views import create_retro_board, board_detail

# Add your urls here.

urlpatterns = [
    path('create-board/', create_retro_board, name='create_retro_board'),
    path('<str:unique_address>/', board_detail, name='board_detail'),
]
