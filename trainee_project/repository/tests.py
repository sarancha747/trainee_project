import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import File, FileHash
from .views import repository

# Create your tests here.

User = get_user_model()


class FileSaveTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username='testuser1')
        self.user1.set_password('password')
        self.user1.save()
        self.user2 = User.objects.create(username='testuser2')
        self.user2.set_password('password')
        self.user2.save()
        self.test_file_dir = os.path.join(os.path.dirname(settings.PROJECT_DIR), settings.TEST_FILE_DIR)
        self.file_dir = os.path.join(os.path.dirname(settings.PROJECT_DIR), settings.FILE_DIR)
        self.test_file_name_1 = 'equal_file_1.txt'
        self.test_file_name_2 = 'equal_file_2.txt'

    def test_first_client_upload(self):
        def add_first_file():
            self.client.login(username='testuser1', password="password")
            get_response = self.client.get('')
            self.assertEqual(200, get_response.status_code)
            with open(os.path.join(self.test_file_dir, self.test_file_name_1), 'rb') as test_file_1:
                data = {'title': '1_test_title', 'description': '1_test_description', 'upload': test_file_1}
                post_response = self.client.post('', data)
                self.assertEqual(200, post_response.status_code)
            file = File.objects.get(title='1_test_title')
            self.assertEqual('1_test_title', file.title)
            self.assertEqual('1_test_description', file.description)
            self.assertEqual('equal_file_1.txt', file.user_file_title)

        def add_second_file():
            self.client.login(username='testuser2', password="password")
            get_response = self.client.get('')
            self.assertEqual(200, get_response.status_code)
            with open(os.path.join(self.test_file_dir, self.test_file_name_2), 'rb') as test_file_2:
                data = {'title': '2_test_title', 'description': '2_test_description', 'upload': test_file_2}
                post_response = self.client.post('', data)
                self.assertEqual(200, post_response.status_code)
            file = File.objects.get(title='2_test_title')
            self.assertEqual('2_test_title', file.title)
            self.assertEqual('2_test_description', file.description)
            self.assertEqual('equal_file_2.txt', file.user_file_title)

        add_first_file()
        add_second_file()

        first_hash = File.objects.get(title='1_test_title')
        second_hash = File.objects.get(title='2_test_title')
        self.assertEqual(first_hash.upload.file_hash, second_hash.upload.file_hash)

        self.assertIn(self.test_file_name_1, os.listdir(self.file_dir))
        self.assertEqual(len(os.listdir(self.file_dir)), 1)
