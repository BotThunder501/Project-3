from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm
from datetime import datetime

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            user=self.user,
            priority='M',
            status='P',
            due_date=datetime.strptime('2025-02-20', '%Y-%m-%d').date()
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.user.username, 'testuser')
        self.assertEqual(self.task.priority, 'M')
        self.assertEqual(self.task.status, 'P')
        self.assertEqual(self.task.due_date, datetime.strptime('2025-02-20', '%Y-%m-%d').date())

    def test_task_str_method(self):
        self.assertEqual(str(self.task), 'Test Task')

class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            user=self.user,
            priority='M',
            status='P',
            due_date=datetime.strptime('2025-02-20', '%Y-%m-%d').date()
        )

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        response = self.client.post(reverse('task_create'), {
            'title': 'New Task',
            'description': 'New Description',
            'priority': 'H',
            'status': 'P',
            'due_date': '2025-02-20'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_edit_view(self):
        response = self.client.post(reverse('task_edit', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': 'L',
            'status': 'D',
            'due_date': '2025-02-20'
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

class TaskFormTest(TestCase):
    def test_valid_form(self):
        form = TaskForm(data={
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'M',
            'status': 'P',
            'due_date': '2025-02-20'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = TaskForm(data={'title': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)