from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('administrateur', 'Administrateur'),
        ('participant', 'Participant'),
        ('organisateur', 'Organisateur'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')

    def __str__(self):
        return f"{self.username} - {self.role}"