from django.db import models
from django.conf import settings
from Evenements.models import Evenement

class Rappel(models.Model):
    
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    message = models.TextField()
    date_rappel = models.DateTimeField(auto_now_add=True)
    envoye = models.BooleanField(default=False)
#retourne une représentation lisible du rappel
    def __str__(self):
        return f"Rappel - {self.evenement.titre}"