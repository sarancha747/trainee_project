import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import File

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
        self.first_file_and_user = {
            'username': 'testuser1',
            'password': 'password',
            'title': '1_test_title',
            'description': '1_test_description',
            'test_file_name': 'equal_file_1.txt'
        }
        self.second_file_and_user = {
            'username': 'testuser2',
            'password': 'password',
            'title': '2_test_title',
            'description': '2_test_description',
            'test_file_name': 'equal_file_2.txt'
        }

        def equal_testfile_create(path):
            try:
                with open(path, "w") as file:
                    file.write("Text Pext")
            except Exception as e:
                print('Ошибка при создании %s. Причина: %s' % (path, e))

        equal_testfile_create(os.path.join(self.test_file_dir, self.first_file_and_user['test_file_name']))
        equal_testfile_create(os.path.join(self.test_file_dir, self.second_file_and_user['test_file_name']))

    def test_1_one_file_save(self):
        def add_file_for_user(file_and_user):
            self.client.login(username=file_and_user['username'], password=file_and_user['password'])
            get_response = self.client.get('')
            self.assertEqual(200, get_response.status_code)
            with open(os.path.join(self.test_file_dir, file_and_user['test_file_name']), 'rb') as test_file_1:
                data = {'title': file_and_user['title'], 'description': file_and_user['description'],
                        'upload': test_file_1}
                post_response = self.client.post('', data)
                self.assertEqual(200, post_response.status_code)
            file = File.objects.get(title=file_and_user['title'])
            self.assertEqual(file_and_user['title'], file.title)
            self.assertEqual(file_and_user['description'], file.description)
            self.assertEqual(file_and_user['test_file_name'], file.user_file_title)

        add_file_for_user(self.first_file_and_user)
        add_file_for_user(self.second_file_and_user)

        # Проверяем что хеши у двух юзеров одинаковые
        first_hash = File.objects.get(title=self.first_file_and_user['title'])
        second_hash = File.objects.get(title=self.second_file_and_user['title'])
        self.assertEqual(first_hash.upload.file_hash, second_hash.upload.file_hash)

        # Проверяем что один файл в папке
        self.assertIn(self.first_file_and_user['test_file_name'], os.listdir(self.file_dir))
        self.assertEqual(len(os.listdir(self.file_dir)), 1)

    def tearDown(self):
        def del_files_in_dir(path):
            try:
                for filename in os.listdir(path):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            except Exception as e:
                print('Ошибка при удалении %s. Причина: %s' % (file_path, e))

        del_files_in_dir(self.file_dir)
        del_files_in_dir(self.test_file_dir)
