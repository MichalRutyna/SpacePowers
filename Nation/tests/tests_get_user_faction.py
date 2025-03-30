from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory

from Nation.views import *

class GetUserNationsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.test_user = User.objects.create_user(
            username='bob', email='bob@test.com', password='Testbob123'
        )

    def test_many_owners(self):
        nat = Nation.objects.create(name='Nation1', slug='nation1')
        nat2 = Nation.objects.create(name='Nation2', slug='nation2')
        user2 = User.objects.create_user(
            username='bob2', email='bob2@test.com', password='Testbob123'
        )
        Ownership(user=self.test_user, nation=nat).save()
        Ownership(user=user2, nation=nat).save()

        Ownership(user=user2, nation=nat2).save()

        nations = get_user_nations(self.test_user)
        nations2 = get_user_nations(user2)

        self.assertEqual(nations.count(), 1)
        self.assertEqual(nations2.count(), 2)

        self.assertIn(nat, nations)
        self.assertNotIn(nat2, nations)
        self.assertIn(nat, nations2)
        self.assertIn(nat2, nations2)


    def test_get_user_nation_none(self):
        nations = get_user_nations(self.test_user)
        self.assertEqual(len(nations), 0)

    def test_get_user_nation_one(self):
        nat = Nation.objects.create(name='Nation1', slug='nation1')
        Ownership(user=self.test_user, nation=nat).save()

        nations = get_user_nations(self.test_user)

        self.assertEqual(len(nations), 1)
        self.assertIn(nat, nations)

    def test_get_user_nation_two(self):
        nat = Nation.objects.create(name='Nation1', slug='nation1')
        nat2 = Nation.objects.create(name='Nation2', slug='nation2')
        Ownership(user=self.test_user, nation=nat).save()
        Ownership(user=self.test_user, nation=nat2).save()

        nations = get_user_nations(self.test_user)

        self.assertEqual(len(nations), 2)
        self.assertIn(nat, nations)
        self.assertIn(nat2, nations)

    def test_get_user_nation_more(self):
        COUNT = 20
        nations = []
        for i in range(COUNT):
            nations.append(Nation.objects.create(name=f'Nation{i}', slug=f'nation{i}'))
            Ownership(user=self.test_user, nation=nations[i]).save()

        nations = get_user_nations(self.test_user)

        self.assertEqual(len(nations), COUNT)
        for i in range(COUNT):
            self.assertIn(nations[i], nations)