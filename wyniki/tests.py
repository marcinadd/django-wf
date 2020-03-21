# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from wyniki.models import Class, Student


class ClassCreateTests(TestCase):

    def test_create_class(self):
        clazz = {"name": "Ia", "year": "2019"}
        response = self.client.post(reverse("wyniki:classes_create"), clazz)
        saved = Class.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(saved.name, clazz.get("name"))
        self.assertEqual(saved.year, int(clazz.get("year")))


class ClassListTests(TestCase):

    def test_get_classes_when_no_classes(self):
        response = self.client.get(reverse("wyniki:classes_list"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Nie znalaziono żadnej klasy")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_get_clsses(self):
        Class(name="Ia", year=2019).save()
        Class(name="IIb", year=2020).save()
        response = self.client.get(reverse("wyniki:classes_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["object_list"], ["<Class: Ia 2019>", "<Class: IIb 2020>"],
                                 ordered=False)


class ClassDeleteTests(TestCase):

    def test_delete_class_which_exists(self):
        clazz = Class(name="Ia", year=2019)
        clazz.save()
        response = self.client.get(reverse("wyniki:classes_delete", args=(clazz.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Class.objects.all().count(), 0)


class ClassUpdateTests(TestCase):
    def test_update_class_which_exists(self):
        clazz = Class(name="Ia", year=2019)
        clazz.save()
        updated = {"name": "IIa", "year": "2020"}
        response = self.client.post(reverse("wyniki:classes_update", args=(clazz.id,)), updated)
        clazz.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(clazz.name, updated.get("name"))
        self.assertEqual(clazz.year, int(updated.get("year")))


class StudentCreateTests(TestCase):

    def test_create_student(self):
        clazz = Class(name="Ia", year=2020)
        clazz.save()
        student = {"first_name": "John", "last_name": "Smith", "clazz": str(clazz.id)}
        response = self.client.post(reverse("wyniki:students_create"), student)
        saved = Student.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(saved.first_name, student.get("first_name"))
        self.assertEqual(saved.last_name, student.get("last_name"))
        self.assertEqual(saved.clazz, clazz)


class StudentListTests(TestCase):

    def test_get_students_when_no_students(self):
        response = self.client.get(reverse("wyniki:students_list"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Nie znalaziono żadnego ucznia")
        self.assertQuerysetEqual(response.context["object_list"], [])

    def test_get_clsses(self):
        clazzA = Class(name="Ia", year=2019)
        clazzA.save()
        clazzB = Class(name="Ib", year=2020)
        clazzB.save()
        Student(first_name="John", last_name="Smith", clazz=clazzA).save()
        Student(first_name="Adam", last_name="Brown", clazz=clazzB).save()
        response = self.client.get(reverse("wyniki:students_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["object_list"],
                                 ["<Student: John Smith Ia 2019>", "<Student: Adam Brown Ib 2020>"],
                                 ordered=False)


class StudentDeleteTests(TestCase):

    def test_delete_student_which_exists(self):
        student = Student(first_name="John", last_name="Smith")
        student.save()
        response = self.client.get(reverse("wyniki:students_delete", args=(student.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Student.objects.all().count(), 0)


class StudentUpdateTests(TestCase):
    def test_update_student_which_exists(self):
        clazzA = Class(name="Ia", year=2019)
        clazzA.save()
        clazzB = Class(name="Ib", year=2020)
        clazzB.save()
        student = Student(first_name="John", last_name="Smith", clazz=clazzA)
        student.save()
        updated = {"first_name": "Adam", "last_name": "Brown", "clazz": str(clazzB.id)}
        response = self.client.post(reverse("wyniki:students_update", args=(student.id,)), updated)
        student.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(student.first_name, updated.get("first_name"))
        self.assertEqual(student.last_name, updated.get("last_name"))
        self.assertEqual(student.clazz, clazzB)


class ClassWithStudentsTests(TestCase):

    def test_get_class_students_create(self):
        response = self.client.get(reverse("wyniki:classes_create_students"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["formset"])
        self.assertIsNotNone(response.context["class_form"])

    def test_post_students_create(self):
        form_data = {
            "name": "Ia",
            "year": "2020",
            "form-0-first_name": "John",
            "form-0-last_name": "Smith",
            "form-1-first_name": "Adam",
            "form-1-last_name": "Brown",
            'form-TOTAL_FORMS': "2",
            'form-INITIAL_FORMS': "0"
        }
        response = self.client.post(reverse("wyniki:classes_create_students"), form_data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Class.objects.all().count(), 1)
        studentA = Student.objects.get(first_name="John")
        studentB = Student.objects.get(first_name="Adam")
        self.assertEquals(studentA.last_name, "Smith")
        self.assertEquals(studentB.last_name, "Brown")
        clazz = Class.objects.get(name="Ia")
        self.assertEquals(clazz.year, 2020)
