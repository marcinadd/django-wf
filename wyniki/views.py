from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from wyniki.forms import StudentFormSet, ClassForm
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


def create_class_with_students(request):
    if request.method == "GET":
        formset = StudentFormSet(queryset=Student.objects.none())
        class_form = ClassForm()
    elif request.method == "POST":
        formset = StudentFormSet(request.POST)
        class_form = ClassForm(request.POST)
        if class_form.is_valid() and formset.is_valid():
            clazz = class_form.save()
            for form in formset:
                student = form.save(commit=False)
                student.clazz = clazz
                student.save()
        return redirect("wyniki:classes_list")

    context = {
        "formset": formset,
        "class_form": class_form
    }
    return render(request, "wyniki/class_students_add.html", context)
