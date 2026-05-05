from django.urls import path
from .views import inscrire_evenement, desinscrire_evenement, billet

urlpatterns = [
    path('inscrire/<int:id>/', inscrire_evenement, name='inscrire_evenement'),
    path('desinscrire/<int:id>/', desinscrire_evenement, name='desinscrire_evenement'),
    path('billet/<int:inscription_id>/', billet, name='billet'),
]