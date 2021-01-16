from django.contrib import admin
from django.contrib.admin import ModelAdmin
from kassa.models import Film


@admin.register(Film)
class FilmAdmin(ModelAdmin):
    pass

