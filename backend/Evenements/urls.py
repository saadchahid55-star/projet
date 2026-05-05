from categorie import views
from django.urls import path
from .views import (
    liste_evenements,
    detail_evenement,
    creer_evenement,
    modifier_evenement,
    supprimer_evenement,
)
from django.urls import path
from .views import liste_evenements
urlpatterns = [
    path('', liste_evenements, name='liste_evenements'),
    path('<int:id>/', detail_evenement, name='detail_evenement'),
    path('creer/', creer_evenement, name='creer_evenement'),
    path('<int:id>/modifier/', modifier_evenement, name='modifier_evenement'),
    path('<int:id>/supprimer/', supprimer_evenement, name='supprimer_evenement'),
    path('evenements/', liste_evenements, name='liste_evenements'),
    path('supprimer-categorie/<int:id>/', views.supprimer_categorie, name='supprimer_categorie'),
    ]





   
