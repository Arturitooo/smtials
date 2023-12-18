from rest_framework import serializers
from .models import BOARD_FIELDS, RetrospectiveBoard, RetroTicket

# Create your serializers here.

class RetrospectiveBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetrospectiveBoard
        fields = '__all__'
        read_only_fields = ('owner',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically set the queryset for copy_ap_from based on the current user
        user = self.context['request'].user
        self.fields['copy_ap_from'].queryset = RetrospectiveBoard.objects.filter(owner=user)

class RetroTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroTicket
        fields = ['author', 'board', 'ticket_type', 'content', 'is_copied']
        read_only_fields = ['author', 'is_copied']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ticket_type'].validators.append(self.validate_ticket_type)

    def validate_ticket_type(self, value):
        # Assuming the board instance is available in the context
        board = self.context.get('board')
        if board:
            variant_choices = [choices for variant, choices in BOARD_FIELDS if variant == board.variant]
            if variant_choices and value not in variant_choices[0]:
                raise serializers.ValidationError(f"Invalid ticket type. Choose from {variant_choices[0]}.")

        return value

    def create(self, validated_data):
        return RetroTicket.objects.create(**validated_data)