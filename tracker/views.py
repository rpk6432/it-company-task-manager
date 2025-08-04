from django.contrib.auth import get_user_model
from django.db.models import Count, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import TaskForm
from .models import Task, Worker


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "tracker/index.html")


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tracker:task-list")


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        return (
            Task.objects
            .prefetch_related("assignees")
            .select_related("task_type")
        )


class TaskDetailView(generic.DetailView):
    model = Task

    def get_queryset(self) -> QuerySet:
        return (
            Task.objects
            .prefetch_related("assignees__position")
            .select_related("task_type")
        )


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tracker:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tracker:task-list")


class WorkerListView(generic.ListView):
    model = get_user_model()
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        return (
            self.model.objects
            .select_related("position")
            .annotate(task_count=Count("tasks"))
        )


class WorkerDetailView(generic.DetailView):
    model = get_user_model()

    def get_queryset(self) -> QuerySet:
        return (
            self.model.objects
            .select_related("position")
            .prefetch_related("tasks")
        )
