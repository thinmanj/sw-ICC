from django.contrib import admin

from .models import Services


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "url_pattern", "method", "enabled"]


admin.site.register(Services, ServiceAdmin)
