from django.urls import path
from . import views

urlpatterns = [
    path('creer/', views.creer_categorie, name='creer_categorie'),
    path('supprimer/<int:id>/', views.supprimer_categorie, name='supprimer_categorie'),
]