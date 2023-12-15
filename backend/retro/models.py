from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

BOARD_FIELDS = [
    ("Good / Bad", ["Good", "Bad", "Action Points"]),
    ("Good / Bad / Not Good Not Bad", ["Good", "Bad", "Not Good Not Bad", "Action Points"]),
    ("More / Less", ["More", "Less", "Action Points"]),
    ('More / Less / Start / Stop', ["More", "Less", "Start", "Stop", "Action Points"]),
]


class RetrospectiveBoard(models.Model):
    address = models.UUIDField(default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    variant = models.CharField(max_length=50, choices=[(variant[0], variant[0]) for variant in BOARD_FIELDS])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.name

class RetroTicket(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(RetrospectiveBoard, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=50)  # "Good", "Bad", "Action Points", etc.
    content = models.TextField()

    def __str__(self):
        return f"{self.board.name} - {self.ticket_type} - {self.content}"
