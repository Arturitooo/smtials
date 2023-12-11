from rest_framework import serializers
from .models import RetroBoard

# Create your serializers here.

class RetroBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroBoard
        fields = '__all__'
