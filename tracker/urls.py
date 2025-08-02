from django.urls import path

from .views import index, TaskListView

app_name = "tracker"

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
]