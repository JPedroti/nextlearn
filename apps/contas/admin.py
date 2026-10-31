from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "papel", "is_staff")
    list_filter = ("papel",) + UserAdmin.list_filter
    fieldsets = UserAdmin.fieldsets + (("Papel no Chamaleon", {"fields": ("papel",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Papel no Chamaleon", {"fields": ("papel", "first_name", "last_name")}),)
