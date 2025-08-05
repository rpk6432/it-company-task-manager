from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import Task, Position, TaskType
from .forms import (
    TaskForm,
    WorkerCreateForm,
    WorkerUpdateForm,
    WorkerSearchForm,
    TaskSearchForm,
)


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "tracker/index.html")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tracker:task-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        name_query = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(
            initial={"name": name_query}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = (
            Task.objects.prefetch_related("assignees")
            .select_related("task_type")
            .order_by("is_completed", "deadline")
        )
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_queryset(self) -> QuerySet:
        return (
            Task.objects
            .prefetch_related("assignees__position")
            .select_related("task_type")
        )


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tracker:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tracker:task-list")


class MyTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "tracker/task_list.html"
    context_object_name = "task_list"
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        name_query = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(
            initial={"name": name_query}
        )
        context["page_title"] = "My Tasks"
        return context

    def get_queryset(self) -> QuerySet:
        queryset = (
            self.request.user.tasks.all()
            .prefetch_related("assignees")
            .select_related("task_type")
            .order_by("is_completed", "deadline")
        )
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = (
            self.model.objects
            .select_related("position")
            .annotate(task_count=Count("tasks"))
        )

        form = WorkerSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()

    def get_queryset(self) -> QuerySet:
        return (
            self.model.objects
            .select_related("position")
            .prefetch_related("tasks")
        )


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreateForm
    success_url = reverse_lazy("tracker:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("tracker:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("tracker:worker-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 10

class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tracker:position-list")

class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tracker:position-list")

class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("tracker:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "tracker/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 10

class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "tracker/task_type_form.html"
    success_url = reverse_lazy("tracker:task-type-list")

class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "tracker/task_type_form.html"
    success_url = reverse_lazy("tracker:task-type-list")

class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "tracker/task_type_confirm_delete.html"
    success_url = reverse_lazy("tracker:task-type-list")
