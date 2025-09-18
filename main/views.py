from django.shortcuts import render

def home(request):
	return render(request, 'main/home.html')

def registro(request):
	return render(request, 'main/registro.html')

def habitaciones(request):
	return render(request, 'main/habitaciones.html')

def galeria(request):
	return render(request, 'main/galeria.html')

def login(request):
	return render(request, 'main/login.html')
