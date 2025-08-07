from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model

from tracker.forms import (
    WorkerCreateForm,
    TaskForm,
    WorkerSearchForm,
    TaskSearchForm
)


class FormTests(TestCase):
    def test_worker_creation_form_meta(self):
        form = WorkerCreateForm()
        self.assertEqual(form._meta.model, get_user_model())
        self.assertIn("username", form.fields)
        self.assertIn("position", form.fields)

    def test_worker_username_validation(self):
        valid_username = "good_user_123"
        form_valid = WorkerCreateForm(data={"username": valid_username})
        self.assertNotIn("username", form_valid.errors)

        invalid_username = "invalid-username!"
        form_invalid = WorkerCreateForm(data={"username": invalid_username})
        self.assertTrue(form_invalid.has_error("username"))
        self.assertIn("Enter a valid username.", form_invalid.errors["username"][0])

    def test_task_form_assignees_widget(self):
        form = TaskForm()
        self.assertIsInstance(
            form.fields["assignees"].widget,
            forms.CheckboxSelectMultiple
        )

    def test_search_forms_are_valid_when_empty(self):
        self.assertTrue(WorkerSearchForm(data={}).is_valid())
        self.assertTrue(TaskSearchForm(data={}).is_valid())
