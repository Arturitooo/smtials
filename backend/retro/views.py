from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import RetrospectiveBoard, RetroTicket
from .serializers import RetrospectiveBoardSerializer, RetroTicketSerializer

# Create your views here.

class RetrospectiveBoardViewSet(viewsets.ModelViewSet):
    queryset = RetrospectiveBoard.objects.all()
    serializer_class = RetrospectiveBoardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        return RetrospectiveBoard.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RetroTicketViewSet(viewsets.ModelViewSet):
    queryset = RetroTicket.objects.all()
    serializer_class = RetroTicketSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        board_pk = request.data.get('board')
        board_instance = get_object_or_404(RetrospectiveBoard, pk=board_pk)
        serializer = RetroTicketSerializer(data=request.data, context={'board': board_instance})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)