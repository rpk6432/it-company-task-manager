from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date

from tracker.models import Position, TaskType, Task


class ModelsTest(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="QA Engineer")
        self.assertEqual(str(position), "QA Engineer")

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Testing")
        self.assertEqual(str(task_type), "Testing")

    def test_worker_str(self):
        worker = get_user_model().objects.create_user(
            username="testuser",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(str(worker), "testuser (John Doe)")

    def test_task_str(self):
        task_type = TaskType.objects.create(name="Development")
        task = Task.objects.create(
            name="Implement feature X",
            description="Details here",
            deadline=date.today(),
            task_type=task_type,
        )
        self.assertEqual(str(task), "Implement feature X")

    def test_worker_get_absolute_url(self):
        worker = get_user_model().objects.create_user(username="test_url_worker")
        expected_url = reverse("tracker:worker-detail", kwargs={"pk": worker.pk})
        self.assertEqual(worker.get_absolute_url(), expected_url)
