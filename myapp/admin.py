from django.contrib import admin
from .models import UserRole, Branch, Asset


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "branch")
    list_filter = ("role",)
    search_fields = ("user__username",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "city", "region", "manager_name", "status")
    list_filter = ("status", "region")
    search_fields = ("name", "code")


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("asset_id", "name", "category", "branch", "status", "condition")
    list_filter = ("category", "status", "condition", "branch")
    search_fields = ("asset_id", "name", "serial_number")
    readonly_fields = ("asset_id", "created_by", "created_at", "updated_at")
