from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse
from stronghold.decorators import public


@public
def login(request):
    return render(request, "users/login.html")


@public
def logout_from_app(request):
    logout(request)
    messages.info(request, "Zostałeś wylogowany!")
    return redirect(reverse('wyniki:index'))
