from django.test import TestCase
from django.test.utils import override_settings

from Nation.models import *

class NationCreateTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='bob', email='bob@test.com', password='Testbob123'
        )
        self.test_user.save()
        self.client.force_login(self.test_user)

    def test_home_one_nation(self):
        nat = Nation.objects.create(name='Nation1', slug='nation1')
        Ownership(user=self.test_user, nation=nat).save()

        response = self.client.get('/nation/', follow=True)
        self.assertTemplateUsed(response, 'nation/details.html')

    def test_home_more_nations(self):
        nat = Nation.objects.create(name='Nation1', slug='nation1')
        nat2 = Nation.objects.create(name='Nation2', slug='nation2')
        Ownership(user=self.test_user, nation=nat).save()
        Ownership(user=self.test_user, nation=nat2).save()

        response = self.client.get('/nation/', follow=True)
        self.assertTemplateUsed(response, 'nation/home.html')

    def test_home_no_nation(self):
        response = self.client.get('/nation/')
        self.assertTemplateUsed(response, 'nation/no_nation.html')

    def test_details_invalid_slug(self):
        response = self.client.get('/nation/nation1/', follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_details_owner(self):
        nat = Nation.objects.create(name='Nation1', slug='nation1')
        Ownership(user=self.test_user, nation=nat).save()

        response = self.client.get('/nation/nation1/')
        self.assertTemplateUsed(response, 'nation/details.html')

    def test_details_not_owner(self):
        nat = Nation.objects.create(name='Nation1', slug='nation1')

        response = self.client.get('/nation/nation1/', follow=True)
        self.assertTemplateUsed(response, 'nation/foreign_detail.html')

    @override_settings(NATION_CREATION_ALLOWED=False)
    def test_creation_page_not_allowed(self):
        response = self.client.post(reverse("b:nation:create"))
        self.assertTemplateUsed(response, '403.html')

    @override_settings(NATION_CREATION_ALLOWED=True)
    def test_creation_page_allowed(self):
        response = self.client.post(reverse("b:nation:create"))
        self.assertTemplateUsed(response, 'nation/create_nation.html')

