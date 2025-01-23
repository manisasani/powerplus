from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        "email",
        "first_name",
        "age",
        "gender",
        "height",
        "weight",
        "is_active",
        "get_profile_link",
    )
    list_filter = (
        "is_active",
        "gender",
        "profile__activity_level",
        "profile__experience_level",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "age",
                    "gender",
                    "height",
                    "weight",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "age",
                    "gender",
                    "height",
                    "weight",
                ),
            },
        ),
    )

    def get_profile_link(self, obj):
        if hasattr(obj, "profile"):
            url = reverse("admin:accounts_profile_change", args=[obj.profile.id])
            return format_html('<a href="{}">View Profile</a>', url)
        return "-"

    get_profile_link.short_description = "Profile"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "activity_level",
        "experience_level",
        "diet_goal",
        "plan_goal",
    )
    list_filter = ("activity_level", "experience_level", "diet_goal", "plan_goal")
    search_fields = ("user__email", "user__first_name")
    raw_id_fields = ("user",)

    fieldsets = (
        (_("User Information"), {"fields": ("user",)}),
        (
            _("Profile Details"),
            {
                "fields": (
                    "activity_level",
                    "experience_level",
                    "diet_goal",
                    "plan_goal",
                )
            },
        ),
    )
