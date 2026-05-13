from django.contrib import admin
from django.urls import path, include
from Base.views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('admin-dashboard/', dashboard_admin, name='dashboard_admin'),
    path('participant-dashboard/', dashboard_participant, name='dashboard_participant'),
    path('organisateur-dashboard/', dashboard_organisateur, name='dashboard_organisateur'),
    path('evenements/', include('Evenements.urls')),
    path('inscription/', include('Inscription.urls')),
    path('desinscrire/<int:event_id>/', desinscription, name='desinscription'),
    path('', include('Evenements.urls')),
    path('categorie/', include('categorie.urls')),
    path('admin/liste-attente/', liste_attente_admin, name='liste_attente_admin'),
    path('admin/billets/', billets_admin, name='billets_admin'),
    path("utilisateurs/", gestion_utilisateurs, name="gestion_utilisateurs"),
    path("utilisateurs/bloquer/<int:id>/", bloquer_utilisateur, name="bloquer_utilisateur"),
    path("utilisateurs/debloquer/<int:id>/", debloquer_utilisateur, name="debloquer_utilisateur"),
    path("utilisateurs/supprimer/<int:id>/", supprimer_utilisateur, name="supprimer_utilisateur"),
    path('liste-attente/', include('ListeAttente.urls')),

    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)