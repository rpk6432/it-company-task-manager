from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import Task


username_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_]+$',
    message=(
        "Enter a valid username. This value may contain only "
        "letters, numbers, and _ characters."
    )
)


class WorkerCreateForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        min_length=5,
        required=True,
        help_text="",
        validators=[username_validator]
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "position", "email", "first_name", "last_name",
        )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = "__all__"
