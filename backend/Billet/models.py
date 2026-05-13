from django.db import models
from Inscription.models import Inscription
import qrcode
from io import BytesIO
from django.core.files import File


class Billet(models.Model):
    inscription = models.OneToOneField(
        Inscription,
        on_delete=models.CASCADE,
        related_name="billet"
    )
    code = models.CharField(max_length=100, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True)
#retourne une représentation lisible du billet
    def __str__(self):
        return f"Billet {self.code}"
#génère un code QR unique pour chaque billet lors de sa création
    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr_content = f"""
Billet: {self.code}
Client: {self.inscription.utilisateur.username}
Evenement: {self.inscription.evenement.titre}
Date: {self.inscription.evenement.date}
"""

            qr_img = qrcode.make(qr_content)

            buffer = BytesIO()
            qr_img.save(buffer, format="PNG")

            file_name = f"qr_{self.inscription.id}.png"
            self.qr_code.save(file_name, File(buffer), save=False)

        super().save(*args, **kwargs)