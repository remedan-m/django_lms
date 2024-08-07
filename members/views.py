from django.shortcuts import render

# Create your views here.

def login_member(request):
    return render(request, 'authenticate/login.html', {})