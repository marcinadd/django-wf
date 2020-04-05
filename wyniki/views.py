from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from stronghold.decorators import public

from wyniki import strings
from wyniki.forms import StudentFormSet, ClassForm, ResultForm, StudentForm, SportForm
from wyniki.helpers import create_results_list_for_student_and_sport, get_best_result_for_sport
from wyniki.models import Class, Student, Sport, Result


@public
def index(request):
    return render(request, 'wyniki/index.html')


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
    form_class = StudentForm
    success_url = reverse_lazy("wyniki:index")


class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy("wyniki:index")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class StudentUpdate(UpdateView):
    model = Student
    form_class = StudentForm
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
    return render(request, "wyniki/class_create.html", context)


def get_results_for_class(request, class_id, sport_id):
    clazz = Class.objects.get(pk=class_id)
    sport = Sport.objects.get(pk=sport_id)
    students = clazz.student_set.all()
    groups = Result.GROUP_CHOICES

    presentation = []
    for student in students:
        results = create_results_list_for_student_and_sport(sport, student)
        presentation.append({"student": student, "results": results})

    best_results_class_set = Result.objects.filter(sport=sport, student__clazz=clazz).order_by(
        "-value" if sport.more_better else "value")

    context = {
        "presentation": presentation,
        "groups": groups,
        "clazz": clazz,
        "sport": sport,
        "best_result": get_best_result_for_sport(sport),
        "best_result_class": best_results_class_set[0] if len(best_results_class_set) > 0 else None
    }

    return render(request, "wyniki/class_results.html", context)


def get_sports_details_by_class(request, pk):
    clazz = Class.objects.get(pk=pk)
    sports = Sport.objects.all()

    context = {
        "clazz": clazz,
        "sports": sports
    }
    return render(request, "wyniki/class_sports_details.html", context)


def get_students_by_class(request, pk):
    clazz = Class.objects.get(pk=pk)
    students = Student.objects.filter(clazz=clazz)

    context = {
        "clazz": clazz,
        "students": students
    }
    return render(request, "wyniki/class_students.html", context)


class ResultCreate(BSModalCreateView):
    template_name = "wyniki/result_create.html"
    form_class = ResultForm
    success_message = 'Ok!'
    success_url = reverse_lazy('wyniki:index')

    def get_context_data(self, **kwargs):
        kwargs["student"] = get_object_or_404(Student, pk=self.kwargs["student_id"])
        kwargs["sport"] = get_object_or_404(Sport, pk=self.kwargs["sport_id"])
        kwargs["group"] = Result.GROUP_CHOICES[int(self.kwargs["group_id"])]
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.student = get_object_or_404(Student, pk=self.kwargs["student_id"])
        form.instance.sport = get_object_or_404(Sport, pk=self.kwargs["sport_id"])
        form.instance.group = Result.GROUP_CHOICES[self.kwargs["group_id"]][0]
        return super().form_valid(form)

    def get_success_url(self):
        class_id = self.object.student.clazz.id
        sport_id = self.object.sport.id
        return reverse("wyniki:classes_results", args=(class_id, sport_id))


class ResultUpdate(BSModalUpdateView):
    template_name = "wyniki/result_update.html"
    form_class = ResultForm
    model = Result
    success_message = 'Ok!'

    def get_success_url(self):
        class_id = self.object.student.clazz.id
        sport_id = self.object.sport.id
        return reverse("wyniki:classes_results", args=(class_id, sport_id))


class ResultDelete(DeleteView):
    model = Result
    success_url = reverse_lazy('author-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ResultDelete, self).delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("wyniki:classes_results", args=(self.object.student.clazz.id, self.object.sport.id))


class SportCreate(CreateView):
    model = Sport
    form_class = SportForm
    success_url = reverse_lazy("wyniki:sports_list")


class SportList(ListView):
    model = Sport


class SportUpdate(UpdateView):
    model = Sport
    form_class = SportForm
    success_url = reverse_lazy("wyniki:sports_list")


class SportDelete(DeleteView):
    model = Sport
    success_url = reverse_lazy("wyniki:sports_list")


# User results

def get_user_results(request):
    user = request.user
    student = None
    students = Student.objects.filter(first_name=user.first_name, last_name=user.last_name)

    if students.count() == 1:
        student = students[0]
    elif students.count() > 1:
        try:
            student = Student.objects.get(email=user.email)
        except Student.DoesNotExist:
            messages.error(request, strings.ERROR_NO_SAME_NAMES_NO_EMAIL)
        except MultipleObjectsReturned:
            messages.error(request, strings.ERROR_SAME_EMAILS)

    presentation = []
    if student:
        for sport in Sport.objects.all():
            results = create_results_list_for_student_and_sport(sport, student)
            presentation.append({"sport": sport, "results": results, "best_result": get_best_result_for_sport(sport)})
    else:
        messages.error(request, strings.ERROR_USER_DOES_NOT_EXIST.format(user.get_full_name()))

    context = {
        "presentation": presentation,
        "student": student,
        "groups": Result.GROUP_CHOICES
    }
    return render(request, "wyniki/user/user_results.html", context)
