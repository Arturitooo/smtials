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

WARMUP_CHOICES = [
        ('dixit_cards', 'Pick dixit card that describe sprint best'),
        ('gif', 'GIF to describe the sprint'),
        ('mem', 'Mem to describe the sprint'),
        ('emojis', 'Emojis to describe the sprint'),
        ('democracy', 'Scum master provides words, team chooses most accurate'),
        ('associations', 'Provide Music / Movie / Game / Quote association for last sprint'),
        ('1 sentence','Write 1 sentence to describe the sprint'),
        ('1 question','Scrum master provides one question and everyone in team answers it'),
        ('know me better','Write something that people might not know about you'),
        ('2 lies 1 truth','Write 2 lies and 1 truth about yourself'),
]


class RetrospectiveBoard(models.Model):
    address = models.UUIDField(default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    variant = models.CharField(max_length=50, choices=[(variant[0], variant[0]) for variant in BOARD_FIELDS])
    copy_ap_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_boards')
    warmup_activity = models.CharField(max_length=150, choices=WARMUP_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class RetroTicket(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(RetrospectiveBoard, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=50)
    content = models.TextField()
    is_copied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.board.name} - {self.ticket_type} - {self.content}"
        
