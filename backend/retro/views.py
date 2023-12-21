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
        new_board = serializer.save(owner=self.request.user)

        # Copy Action Point RetroTickets from the last retrospective board
        last_board = new_board.copy_ap_from
        if last_board:
            action_point_tickets = RetroTicket.objects.filter(board=last_board, ticket_type='Action Points')
            for ticket in action_point_tickets:
                RetroTicket.objects.create(
                    author=ticket.author,
                    board=new_board,
                    ticket_type=ticket.ticket_type,
                    content=ticket.content,
                    is_copied=True,
                )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the user making the request is the owner of the board
        if request.user != instance.owner:
            return Response(
                {"detail": "You do not have permission to delete this board."},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class RetroTicketViewSet(viewsets.ModelViewSet):
    queryset = RetroTicket.objects.all()
    serializer_class = RetroTicketSerializer
    
    # TO DO - LIST OF TICKETS ONLY FROM SPECIFIC BOARD

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