from django.db import models 
import sys
sys.path.append("..")
from users.models import User

# Create your models here.
class Room(models.Model):
    participants = models.ManyToManyField(User, related_name="participants")
    room = models.CharField(max_length=200, null=True)
    game_active = models.BooleanField(default=False)

    def __str__(self):
        return self.room
