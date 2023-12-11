# retro/urls.py
from django.urls import path
from .views import RetroBoardCreateView

urlpatterns = [
    path('create-board/', RetroBoardCreateView.as_view(), name='create-board'),
]
