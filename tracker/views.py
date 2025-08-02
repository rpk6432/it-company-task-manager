from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import TaskForm
from .models import Task


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "tracker/index.html")


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tracker:task-list")


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 10
