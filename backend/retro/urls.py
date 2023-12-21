from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RetrospectiveBoardViewSet, RetroTicketViewSet

router = DefaultRouter()
router.register(r'board', RetrospectiveBoardViewSet, basename='board')
router.register(r'ticket', RetroTicketViewSet, basename='ticket')

# Add your urls here.

urlpatterns = [
    path('', include(router.urls)),
]
