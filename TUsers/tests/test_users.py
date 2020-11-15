from django.test import TestCase
from TUsers.models import TUser

class TUserTestCase(TestCase):
    def setUp(self):
        TUser.objects.create(username="mark_cuban",password="sharktank",country="USA")
    def test_create(self):
        self.assertEqual("USA",TUser.objects.get(username="mark_cuban").country)