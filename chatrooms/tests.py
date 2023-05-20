from django.test import TestCase
from chatrooms.models import CustomUser, Room
# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        obj = CustomUser(username='testuser', user_name='テストユーザー', memo='None.')
        obj.save()


    def test_record_count(self):
        qs_count = CustomUser.objects.count()
        self.assertEqual(qs_count, 1)

"""
class RoomTestCase(TestCase):
    def setup(self):
        user = CustomUser(username='testuser', user_name='テストユーザー', memo='None.')
        user.save()

    def test_user_exist(self):
        qs_count = CustomUser.objects.count()
        self.assertEqual(qs_count, 1)

    def test_create_room(self):
        room1 = Room(title='no_title', user=CustomUser.objects.get(username='testuser'))
        room1.save()
        room2 = Room(title='undifined_title', user=CustomUser.objects.get(username='testuser'))
        room2.save()

        qs_count = Room.objects.count()
        self.assertEqual(qs_count,2)
"""