from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from wyniki.models import Class


def index(request):
    return render(request, 'wyniki/index.html')


class ClassCreate(CreateView):
    model = Class
    fields = ["name", "year"]
    success_url = "/"


class ClassList(ListView):
    model = Class
