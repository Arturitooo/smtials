from django.db import models
from django.contrib.auth.models import User

# Create your models here.

BOARD_VARIANTS = [
    ("GoodBad", "Good / Bad"),
    ("GoodBadNotgoodnotbad", "Good / Bad / Not good not bad"),
    ("MoreLess", "More / Less"),
    ('MoreLessStartStop', "More / Less / Start / Stop"),
]


class RetroBoard(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    variant = models.CharField(max_length=250, choices=BOARD_VARIANTS)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name