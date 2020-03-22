from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from wyniki.forms import StudentFormSet, ClassForm
from wyniki.models import Class, Student, Sport, Result, Group


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


def get_results_for_class(request, class_id, sport_id):
    clazz = Class.objects.get(pk=class_id)
    sport = Sport.objects.get(pk=sport_id)
    students = clazz.student_set.all()
    groups = Group.objects.all()

    presentation = []
    for student in students:
        presentation.append({"student": student, "results": []})

    for group in groups:
        group_results = Result.objects.filter(student__clazz=clazz, sport=sport, group=group)
        student_result = {}
        for result in group_results:
            student_result[result.student] = result
        for obj in presentation:
            student = obj.get("student")
            result = student_result.get(student)
            obj["results"].append({"group": group, "result": result})

    return render(request, "wyniki/class_results.html", {"presentation": presentation})
