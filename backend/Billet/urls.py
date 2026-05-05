from django.urls import path
from .views import voir_billet

urlpatterns = [
    path('<int:id>/', voir_billet, name='voir_billet'),
]