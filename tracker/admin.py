from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Position, TaskType, Worker, Task


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "position",
                )
            },
        ),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "task_type",
        "priority",
        "deadline",
        "is_completed"
    )
    search_fields = ("name",)
    list_filter = ("priority", "is_completed", "task_type")

    filter_horizontal = ("assignees",)


admin.site.register(Position)
admin.site.register(TaskType)
