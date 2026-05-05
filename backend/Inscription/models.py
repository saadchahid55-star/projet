from django.db import models
from django.conf import settings
from Evenements.models import Evenement

class Inscription(models.Model):
    STATUT_CHOICES = [
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
    ]

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inscriptions'
    )
    evenement = models.ForeignKey(
        Evenement,
        on_delete=models.CASCADE,
        related_name='inscriptions'
    )
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='confirme')
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'evenement')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.evenement.titre}"