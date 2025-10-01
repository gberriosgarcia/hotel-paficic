# usuarios/urls.py
from xml.etree.ElementInclude import include
from django.urls import path
from .views import EmailLoginView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', include('usuarios.urls')),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('registro/', views.registro, name='registro'),
]
