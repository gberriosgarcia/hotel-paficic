"""
URL configuration for hotel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# hotel_project/urls.py
from django.contrib import admin
from django.urls import path
from main import views
from usuarios.views import EmailLoginView  # <- importa tu vista
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('habitaciones/', views.habitaciones, name='habitaciones'),
    path('galeria/', views.galeria, name='galeria'),
    path('login/', EmailLoginView.as_view(), name='login'),  # <- aquí el cambio
    path('reservar/', views.reservar, name='reservar'),
    path('login/', EmailLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # <-- ESTA LÍNEA
]


