# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from wyniki.models import Class, Student, Result, Sport

studentA_first_name = "John"
studentA_last_name = "Smith"

studentB_first_name = "Adam"
studentB_last_name = "Brown"


class IndexTests(TestCase):
    def test_index_without_auth_ok(self):
        response = self.client.get(reverse("wyniki:index"))
        self.assertEquals(response.status_code, 200)


class SuperUserTestCase(TestCase):

    def setUp(self):
        User.objects.create_superuser(username='superuser', password='password')
        self.client.login(username='superuser', password='password')


class ClassListTests(SuperUserTestCase):
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


class ClassDeleteTests(SuperUserTestCase):
    def test_delete_class_which_exists(self):
        clazz = Class(name="Ia", year=2019)
        clazz.save()
        response = self.client.get(reverse("wyniki:classes_delete", args=(clazz.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Class.objects.all().count(), 0)


class ClassUpdateTests(SuperUserTestCase):
    def test_update_class_which_exists(self):
        clazz = Class(name="Ia", year=2019)
        clazz.save()
        updated = {"name": "IIa", "year": "2020"}
        response = self.client.post(reverse("wyniki:classes_update", args=(clazz.id,)), updated)
        clazz.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(clazz.name, updated.get("name"))
        self.assertEqual(clazz.year, int(updated.get("year")))


class StudentCreateTests(SuperUserTestCase):
    def test_create_student(self):
        clazz = Class(name="Ia", year=2020)
        clazz.save()
        student = {"first_name": studentA_first_name, "last_name": studentA_last_name, "clazz": str(clazz.id)}
        response = self.client.post(reverse("wyniki:students_create"), student)
        saved = Student.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(saved.first_name, student.get("first_name"))
        self.assertEqual(saved.last_name, student.get("last_name"))
        self.assertEqual(saved.clazz, clazz)


class StudentListTests(SuperUserTestCase):
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
        Student(first_name=studentA_first_name, last_name=studentA_last_name, clazz=clazzA).save()
        Student(first_name=studentB_first_name, last_name=studentB_last_name, clazz=clazzB).save()
        response = self.client.get(reverse("wyniki:students_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["object_list"],
                                 ["<Student: John Smith Ia 2019>", "<Student: Adam Brown Ib 2020>"],
                                 ordered=False)


class StudentDeleteTests(SuperUserTestCase):
    def test_delete_student_which_exists(self):
        student = Student(first_name=studentA_first_name, last_name=studentA_last_name)
        student.save()
        response = self.client.get(reverse("wyniki:students_delete", args=(student.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Student.objects.all().count(), 0)


class StudentUpdateTests(SuperUserTestCase):
    def test_update_student_which_exists(self):
        clazzA = Class(name="Ia", year=2019)
        clazzA.save()
        clazzB = Class(name="Ib", year=2020)
        clazzB.save()
        student = Student(first_name=studentA_first_name, last_name=studentA_last_name, clazz=clazzA)
        student.save()
        updated = {"first_name": studentB_first_name, "last_name": studentB_last_name, "clazz": str(clazzB.id)}
        response = self.client.post(reverse("wyniki:students_update", args=(student.id,)), updated)
        student.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(student.first_name, updated.get("first_name"))
        self.assertEqual(student.last_name, updated.get("last_name"))
        self.assertEqual(student.clazz, clazzB)


class ClassWithStudentsTests(SuperUserTestCase):
    def test_get_class_students_create(self):
        response = self.client.get(reverse("wyniki:classes_create"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["formset"])
        self.assertIsNotNone(response.context["class_form"])

    def test_post_students_create(self):
        form_data = {
            "name": "Ia",
            "year": "2020",
            "form-0-first_name": studentA_first_name,
            "form-0-last_name": studentA_last_name,
            "form-1-first_name": studentB_first_name,
            "form-1-last_name": studentB_last_name,
            'form-TOTAL_FORMS': "2",
            'form-INITIAL_FORMS': "0"
        }
        response = self.client.post(reverse("wyniki:classes_create"), form_data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Class.objects.all().count(), 1)
        studentA = Student.objects.get(first_name=studentA_first_name)
        studentB = Student.objects.get(first_name=studentB_first_name)
        self.assertEquals(studentA.last_name, studentA_last_name)
        self.assertEquals(studentB.last_name, studentB_last_name)
        clazz = Class.objects.get(name="Ia")
        self.assertEquals(clazz.year, 2020)


class ClassResultsTests(SuperUserTestCase):
    def test_results_for_class_with_exists(self):
        clazz = Class.objects.create(name="Ia", year=2020)
        studentA = Student.objects.create(first_name=studentA_first_name, last_name=studentA_last_name, clazz=clazz)
        studentB = Student.objects.create(first_name=studentB_first_name, last_name=studentB_last_name, clazz=clazz)
        sport = Sport.objects.create(name="sample")
        resultA = Result.objects.create(value=3.5, sport=sport, student=studentA, group=Result.FIRST)
        resultB = Result.objects.create(value=4.5, sport=sport, student=studentB, group=Result.FIRST)
        resultC = Result.objects.create(value=5.5, sport=sport, student=studentB, group=Result.SECOND)
        response = self.client.get(reverse("wyniki:classes_results", args=(clazz.id, sport.id,)))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, resultA.value)
        self.assertContains(response, resultB.value)
        self.assertContains(response, resultC.value)
        self.assertIsNotNone(response.context["presentation"])
        self.assertIsNotNone(response.context["groups"])
        self.assertIsNotNone(response.context["clazz"])
        self.assertIsNotNone(response.context["sport"])


class SportDetailsTests(SuperUserTestCase):
    def test_get_details_for_specified_class(self):
        clazz = Class.objects.create(name="Ia", year=2019)
        sport = Sport.objects.create(name="sample")
        response = self.client.get(reverse("wyniki:classes_sports", args=[clazz.id, ]))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["clazz"], clazz)
        self.assertEquals(response.context["sports"].count(), 1)


class StudentsByClassTests(SuperUserTestCase):
    def test_get_students_by_class(self):
        clazz = Class.objects.create(name="Ia", year=2019)
        Student.objects.create(first_name=studentA_first_name, last_name=studentA_last_name, clazz=clazz)
        Student.objects.create(first_name=studentB_first_name, last_name=studentB_last_name, clazz=clazz)
        response = self.client.get(reverse("wyniki:classes_students", args=(clazz.id,)))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["clazz"], clazz)
        self.assertEquals(response.context["students"].count(), 2)


class CreateResultTests(SuperUserTestCase):
    def test_create_result_ok(self):
        value = 1.25
        clazz = Class.objects.create(name="Ia", year=2019)
        student = Student.objects.create(first_name=studentA_first_name, last_name=studentA_last_name, clazz=clazz)
        sport = Sport.objects.create(name="sample")
        self.client.post(reverse("wyniki:results_create", args=(student.id, sport.id, 0)), {"value": value})
        result = Result.objects.get()
        self.assertEquals(result.student, student)
        self.assertEquals(result.sport, sport)
        self.assertEquals(result.value, value)


def create_sample_result():
    value = 1.25
    clazz = Class.objects.create(name="Ia", year=2019)
    student = Student.objects.create(first_name=studentA_first_name, last_name=studentA_last_name, clazz=clazz)
    sport = Sport.objects.create(name="sample")
    return Result.objects.create(value=value, student=student, sport=sport, group=Result.FIRST)


class UpdateResultTests(SuperUserTestCase):
    def test_update_result_ok(self):
        result = create_sample_result()
        response = self.client.post(reverse("wyniki:results_update", args=(result.id,)), {"value": 1.5})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Result.objects.get(id=result.id).value, 1.5)


class DeleteResultTests(SuperUserTestCase):
    def test_delete_result_ok(self):
        result = create_sample_result()
        response = self.client.post(reverse("wyniki:results_delete", args=(result.id,)))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Result.objects.all().count(), 0)


class SportListTests(SuperUserTestCase):
    def test_list_ok(self):
        Sport.objects.create(name="sampleA", unit="m", more_better=True)
        Sport.objects.create(name="sampleB", unit="m", more_better=False)
        response = self.client.get(reverse("wyniki:sports_list"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["object_list"].count(), 2)


class SportUpdateTests(SuperUserTestCase):
    def test_update_ok(self):
        sport = Sport.objects.create(name="sampleA", unit="m", more_better=True)
        response = self.client.post(reverse("wyniki:sports_update", args=(sport.id,)),
                                    {"name": "updated", "more_better": "False", "unit": "kg"})
        sport.refresh_from_db()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(sport.name, "updated")
        self.assertEquals(sport.unit, "kg")
        self.assertEquals(sport.more_better, False)


class SportDeleteTests(SuperUserTestCase):
    def test_delete_ok(self):
        sport = Sport.objects.create(name="sampleA", unit="m", more_better=True)
        response = self.client.post(reverse("wyniki:sports_delete", args=(sport.id,)))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Sport.objects.all().count(), 0)
