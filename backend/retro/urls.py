from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RetrospectiveBoardViewSet, RetroTicketViewSet

router = DefaultRouter()
router.register(r'retrospective-board', RetrospectiveBoardViewSet, basename='retrospective-board')
router.register(r'retro-tickets', RetroTicketViewSet, basename='retro-ticket')

# Add your urls here.

urlpatterns = [
    path('api/', include(router.urls)),
]
