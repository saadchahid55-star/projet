from django.db import models
from django.conf import settings
from Evenements.models import Evenement

class ListeAttente(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='liste_attente')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'evenement')

    def __str__(self):
        return f"{self.utilisateur.username} en attente pour {self.evenement.titre}"