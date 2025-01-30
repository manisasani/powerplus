from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, DietPlanInfo, WorkoutPlanInfo
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class DietPlanInfoInline(admin.StackedInline):
    model = DietPlanInfo
    can_delete = False
    verbose_name_plural = "Diet Plan Info"

class WorkoutPlanInfoInline(admin.StackedInline):
    model = WorkoutPlanInfo
    can_delete = False
    verbose_name_plural = "Workout Plan Info"

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, DietPlanInfoInline, WorkoutPlanInfoInline)
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
        "diet_info__activity_level", 
        "workout_info__experience_level",  
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
        if hasattr(obj, "main_profile"): 
            url = reverse("admin:accounts_profile_change", args=[obj.main_profile.id])
            return format_html('<a href="{}">View Profile</a>', url)
        return "-"

    get_profile_link.short_description = "Profile"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "get_activity_level",
        "get_experience_level",
        "get_diet_goal",
        "get_plan_goal",
    )
    list_filter = (
        "data_diet__activity_level",
        "data_plan__experience_level",
        "data_diet__diet_goal",
        "data_plan__plan_goal",
    )
    search_fields = ("user__email", "user__first_name")
    raw_id_fields = ("user",)

    def get_activity_level(self, obj):
        return obj.data_diet.activity_level if obj.data_diet else "-"
    get_activity_level.short_description = "Activity Level"

    def get_experience_level(self, obj):
        return obj.data_plan.experience_level if obj.data_plan else "-"
    get_experience_level.short_description = "Experience Level"

    def get_diet_goal(self, obj):
        return obj.data_diet.diet_goal if obj.data_diet else "-"
    get_diet_goal.short_description = "Diet Goal"

    def get_plan_goal(self, obj):
        return obj.data_plan.plan_goal if obj.data_plan else "-"
    get_plan_goal.short_description = "Plan Goal"


@admin.register(DietPlanInfo)
class DietPlanInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "activity_level", "diet_goal")
    list_filter = ("activity_level", "diet_goal")
    search_fields = ("user__email", "user__first_name")


@admin.register(WorkoutPlanInfo)
class WorkoutPlanInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "experience_level", "plan_goal")
    list_filter = ("experience_level", "plan_goal")
    search_fields = ("user__email", "user__first_name")