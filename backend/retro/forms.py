# retro/forms.py
from django import forms
from django.forms.models import modelform_factory
from .models import BOARD_FIELDS, RetroTicket

class RetroTicketForm(forms.ModelForm):
    ticket_type = forms.CharField(widget=forms.HiddenInput(), required=False)  # Hidden field for ticket_type
    class Meta:
        model = RetroTicket
        fields = ['content', 'ticket_type']


def get_ticket_forms(variant):
    ticket_forms = []
    matching_field = next((values for field, values in BOARD_FIELDS if field == variant), None)
    for ticket_type in matching_field:
        TicketForm = modelform_factory(
            RetroTicket, 
            fields=['content', 'ticket_type'],
            labels={'content': ticket_type},
            widgets={'ticket_type': forms.HiddenInput(attrs={'value': ticket_type})}
        )
        ticket_forms.append(TicketForm)

    return ticket_forms