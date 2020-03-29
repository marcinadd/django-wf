from bootstrap_modal_forms.forms import BSModalForm
from django import forms
from django.forms import modelformset_factory

from wyniki.models import Class, Student, Result, Sport


class ClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        add_bootstrap_classes(self.fields)

    class Meta:
        model = Class
        fields = {"name", "year"}
        labels = {
            "name": "Nazwa",
            "year": "Rok"
        }


StudentFormSet = modelformset_factory(
    Student, extra=3, fields=("first_name", "last_name"),
    labels={
        "first_name": "Imię ucznia",
        "last_name": "Nazwisko ucznia",
    }
)


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        add_bootstrap_classes(self.fields)

    class Meta:
        model = Student
        fields = ["first_name", "last_name", "clazz"]
        labels = {
            "first_name": "Imię",
            "last_name": "Nazwisko",
            "clazz": "Klasa"
        }


class SportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SportForm, self).__init__(*args, **kwargs)
        add_bootstrap_classes(self.fields)

    class Meta:
        model = Sport
        fields = {"name", "unit", "more_better"}
        labels = {
            "name": "Nazwa",
            "unit": "Jednostka",
            "more_better": "Więcej lepiej: "
        }


class ResultForm(BSModalForm):
    class Meta:
        model = Result
        fields = {"value"}


def add_bootstrap_classes(fields):
    for field in iter(fields):
        fields[field].widget.attrs.update({
            'class': 'form-control'
        })
