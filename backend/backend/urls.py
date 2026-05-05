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
    path('client-dashboard/', dashboard_client, name='dashboard_client'),

    path('evenements/', include('Evenements.urls')),
    path('inscription/', include('Inscription.urls')),
    path('desinscrire/<int:event_id>/', desinscription, name='desinscription'),
    path('', include('Evenements.urls')),
    path('categorie/', include('categorie.urls')),
    path('admin/liste-attente/', liste_attente_admin, name='liste_attente_admin'),
    path('admin/billets/', billets_admin, name='billets_admin'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
