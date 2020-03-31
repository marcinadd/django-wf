from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.
from django.urls import reverse


def wyloguj(request):
    logout(request)
    messages.info(request, "Zostałeś wylogowany!")
    return redirect(reverse('wyniki:index'))
