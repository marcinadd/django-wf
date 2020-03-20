from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from wyniki.models import Class, Student


def index(request):
    return render(request, 'wyniki/index.html')


class ClassCreate(CreateView):
    model = Class
    fields = ["name", "year"]
    success_url = reverse_lazy("wyniki:index")


class ClassList(ListView):
    model = Class


class ClassDelete(DeleteView):
    model = Class
    success_url = reverse_lazy("wyniki:index")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ClassUpdate(UpdateView):
    model = Class
    fields = ["name", "year"]
    success_url = reverse_lazy("wyniki:index")


class StudentCreate(CreateView):
    model = Student
    fields = ["first_name", "last_name", "clazz"]
    success_url = reverse_lazy("wyniki:index")


class StudentList(ListView):
    model = Student


class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy("wyniki:index")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class StudentUpdate(UpdateView):
    model = Student
    fields = ["first_name", "last_name", "clazz"]
    success_url = reverse_lazy("wyniki:index")
