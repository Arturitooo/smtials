from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required

from .forms import RetrospectiveBoardForm, RetroTicketForm, get_ticket_forms
from .models import RetrospectiveBoard, RetroTicket

# Create your views here.

@login_required
def create_retro_board(request):
    if request.method == 'POST':
        form = RetrospectiveBoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return redirect('board_detail', unique_address=str(board.address))
    else:
        form = RetrospectiveBoardForm()

    return render(request, 'retro/create_board.html', {'form': form})

@login_required
def board_detail(request, unique_address):
    board = RetrospectiveBoard.objects.get(address=unique_address)
    ticket_forms = get_ticket_forms(board.variant)

    if request.method == 'POST':
        for TicketForm in ticket_forms:
            form = TicketForm(request.POST)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.author = request.user
                ticket.board = board
                ticket.save()

    form_instances = [TicketForm() for TicketForm in ticket_forms]

    if request.method == 'GET':
        # Return a response for GET requests
        return render(request, 'retro/board_detail.html', {'board': board, 'forms': form_instances})

    return redirect('some_other_view')  # Replace 'some_other_view' with the appropriate redirect