from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from tracker.models import Position


class AdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password123",
            email="admin@example.com"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="testworker",
            password="password123",
            email="worker@example.com",
            position=self.position
        )

    def test_worker_position_in_list_view(self):
        url = reverse("admin:tracker_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.position.name)

    def test_worker_position_in_change_view(self):
        url = reverse("admin:tracker_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, "position")

    def test_worker_position_in_add_view(self):
        url = reverse("admin:tracker_worker_add")
        res = self.client.get(url)
        self.assertContains(res, "position")
