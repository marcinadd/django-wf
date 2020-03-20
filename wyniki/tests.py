# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from wyniki.models import Class


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
        print(response.context["object_list"])
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["object_list"], ["<Class: Ia 2019>", "<Class: IIb 2020>"],
                                 ordered=False)
