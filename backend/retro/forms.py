# retro/forms.py
from django import forms
from django.forms.models import modelform_factory
from .models import BOARD_FIELDS, RetrospectiveBoard, RetroTicket

class RetrospectiveBoardForm(forms.ModelForm):
    class Meta:
        model = RetrospectiveBoard
        fields = ['name', 'variant']

class RetroTicketForm(forms.ModelForm):
    class Meta:
        model = RetroTicket
        fields = ['content']

def get_ticket_forms(variant):
    ticket_forms = []
    matching_field = next((values for field, values in BOARD_FIELDS if field == variant), None)
    for ticket_type in matching_field:
        TicketForm = modelform_factory(RetroTicket, fields=['content'], widgets={'content': forms.HiddenInput()}, labels={'content': ticket_type})
        ticket_forms.append(TicketForm)
    
    print(ticket_forms)
    return ticket_forms