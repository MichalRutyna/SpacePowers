from django.test import TestCase

from Nation.models import Nation


class NationNotLoggedInViews(TestCase):
    def test_home_not_logged_in(self):
        nat = Nation.objects.create(name='Nation1', slug='nation1')
        response = self.client.get('/nation/')
        self.assertRedirects(response, "/account/login/?next=/nation/")

    def test_creation_not_logged_in(self):
        response = self.client.post("/nation/create/")
        self.assertRedirects(response, "/account/login/?next=/nation/create/")

    def test_fields_not_logged_in(self):
        nat = Nation.objects.create(name='Nation1', slug='nation1')
        response = self.client.post("/nation/nation1/fields/")
        self.assertRedirects(response, "/account/login/?next=/nation/nation1/fields/")

    def test_details_not_logged_in(self):
        nat = Nation.objects.create(name='Nation1', slug='nation1')
        response = self.client.get('/nation/nation1/')
        self.assertRedirects(response, "/account/login/?next=/nation/nation1/")