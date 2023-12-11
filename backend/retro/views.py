from rest_framework import generics, permissions
#from .models import RetroBoard
from .serializers import RetroBoardSerializer

# Create your views here.

class RetroBoardCreateView(generics.CreateAPIView):
    serializer_class = RetroBoardSerializer
    permission_classes = [permissions.IsAuthenticated]
