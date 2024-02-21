from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('pj_name', 'pj_code', 'coordinator', 'manager')


# Register your models here.
admin.site.register(Project, ProjectAdmin)
