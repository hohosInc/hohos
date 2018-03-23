from django.shortcuts import render

# Create your views here.

def funhome(request):
	return render(request, 'fun/gattu_barat.html', {}) 

def fungone(request):
	return render(request, 'fun/banned.html', {})