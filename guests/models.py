
from django.db import models

class Guest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    has_arrived = models.BooleanField(default=False)
    number_of_companions = models.PositiveIntegerField(default=0)
    court = models.CharField(max_length=5, null=True)
    row = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"