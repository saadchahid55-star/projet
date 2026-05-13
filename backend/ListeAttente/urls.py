from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_attente, name='liste_attente'),
]