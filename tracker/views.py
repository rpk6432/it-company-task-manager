from django.shortcuts import render
from django.views import generic
from django.http import HttpRequest, HttpResponse

from .models import Task


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "tracker/index.html")


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 10
