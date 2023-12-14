# retro/forms.py
from django import forms
from .models import RetrospectiveBoard, RetroTicket

class RetrospectiveBoardForm(forms.ModelForm):
    class Meta:
        model = RetrospectiveBoard
        fields = ['name', 'variant']

class RetroTicketForm(forms.ModelForm):
    class Meta:
        model = RetroTicket
        fields = ['ticket_type', 'content']

    def __init__(self, *args, **kwargs):
        board_variant_choices = kwargs.pop('board_variant_choices', [])
        super(RetroTicketForm, self).__init__(*args, **kwargs)

        self.fields['ticket_type'] = forms.ChoiceField(
            choices=[(choice, choice) for choice in board_variant_choices]
        )