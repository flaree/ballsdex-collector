from django.contrib import admin

from .models import CollectorType


@admin.register(CollectorType)
class CollectorTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "min", "max", "gap", "source_special", "enabled")
    list_filter = ("enabled",)
    search_fields = ("name",)
