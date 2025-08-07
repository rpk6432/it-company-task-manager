from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tracker.models import Position, TaskType, Task


class PublicAccessTests(TestCase):
    def test_login_required_for_all_pages(self):
        position = Position.objects.create(name="Dev")
        task_type = TaskType.objects.create(name="Bug")
        worker = get_user_model().objects.create_user(
            username="test",
            password="pass",
            email="test@example.com"
        )
        task = Task.objects.create(
            name="Fix bug", deadline=date.today(), task_type=task_type
        )

        urls = [
            reverse("tracker:index"),
            reverse("tracker:task-list"),
            reverse("tracker:task-create"),
            reverse("tracker:task-detail", args=[task.pk]),
            reverse("tracker:task-update", args=[task.pk]),
            reverse("tracker:task-delete", args=[task.pk]),
            reverse("tracker:my-task-list"),
            reverse("tracker:worker-list"),
            reverse("tracker:worker-detail", args=[worker.pk]),
            reverse("tracker:worker-create"),
            reverse("tracker:worker-update", args=[worker.pk]),
            reverse("tracker:worker-delete", args=[worker.pk]),
            reverse("tracker:position-list"),
            reverse("tracker:position-create"),
            reverse("tracker:position-update", args=[position.pk]),
            reverse("tracker:position-delete", args=[position.pk]),
            reverse("tracker:task-type-list"),
            reverse("tracker:task-type-create"),
            reverse("tracker:task-type-update", args=[task_type.pk]),
            reverse("tracker:task-type-delete", args=[task_type.pk]),
            reverse("tracker:task-toggle-status", args=[task.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse("login"), response.url)


class PrivateAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")
        cls.task_type = TaskType.objects.create(name="Feature")
        cls.worker1 = get_user_model().objects.create_user(
            username="worker1",
            password="password123",
            email="worker1@example.com",
            position=cls.position,
        )
        cls.worker2 = get_user_model().objects.create_user(
            username="worker2",
            password="password123",
            email="worker2@example.com",
            position=cls.position,
        )
        cls.task = Task.objects.create(
            name="Develop new feature",
            deadline=date.today(),
            task_type=cls.task_type,
        )
        cls.task.assignees.add(cls.worker1)

    def setUp(self):
        self.client.force_login(self.worker1)

    def test_search_functionality(self):
        """Test that search forms correctly filter list views."""
        response = self.client.get(
            reverse("tracker:worker-list"), {"username": "worker1"}
        )
        self.assertIn(self.worker1, response.context["object_list"])
        self.assertNotIn(self.worker2, response.context["object_list"])

    def test_my_tasks_list_shows_only_assigned_tasks(self):
        response = self.client.get(reverse("tracker:my-task-list"))
        self.assertIn(self.task, response.context["task_list"])

        # Log in as worker2, who is NOT assigned to the task, and check again
        self.client.force_login(self.worker2)
        response = self.client.get(reverse("tracker:my-task-list"))
        self.assertNotIn(self.task, response.context["task_list"])

    def test_toggle_task_status_view(self):
        """Test that POSTing to the toggle view flips the task's status."""
        toggle_url = reverse("tracker:task-toggle-status", args=[self.task.pk])

        self.assertFalse(self.task.is_completed)

        # First toggle: False -> True
        self.client.post(toggle_url)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

        # Second toggle: True -> False
        self.client.post(toggle_url)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)
