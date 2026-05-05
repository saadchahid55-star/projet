from django.urls import path
from .views import HomeView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]