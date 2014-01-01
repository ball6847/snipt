from django.contrib import admin
from .models import Job


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'company', 'url',)
    ordering = ('-created',)

admin.site.register(Job, JobAdmin)
