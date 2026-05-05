from django.db import models
from Inscription.models import Inscription

class Billet(models.Model):
    inscription = models.OneToOneField(Inscription, on_delete=models.CASCADE, related_name='billet')
    code = models.CharField(max_length=100, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billet {self.code}"