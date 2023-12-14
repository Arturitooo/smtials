from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import RetrospectiveBoardForm, RetroTicketForm
from .models import RetrospectiveBoard

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
    board_variant_choices = [choice[0] for choice in board.BOARD_FIELDS[0][1]]

    if request.method == 'POST':
        form = RetroTicketForm(request.POST, board_variant_choices=board_variant_choices)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.board = board
            ticket.save()
            return redirect('board_detail', unique_address=unique_address)
    else:
        form = RetroTicketForm(board_variant_choices=board_variant_choices)

    return render(request, 'retro/board_detail.html', {'board': board, 'form': form})