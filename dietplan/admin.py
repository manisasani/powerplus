from django.contrib import admin
from .models import DietPlan, UserSelectedDietPlan
from django.core.exceptions import ValidationError
@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ('goal', 'calorie_range_min', 'calorie_range_max', 'created_at')
    list_filter = ('goal',)
    search_fields = ('goal', 'notes')
    fieldsets = (
        ('Basic Info', {
            'fields': ('goal', 'calorie_range_min', 'calorie_range_max')
        }),
        ('Macros', {
            'fields': ('protein_percentage', 'carbs_percentage', 'fat_percentage')
        }),
        ('Meals', {
            'fields': ('breakfast','snacks', 'lunch','snacks2', 'dinner', 'snacks3')
        }),
        ('Additional Info', {
            'fields': ('notes',)
        }),
    )

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            from django.contrib import messages
            messages.error(request, str(e))
            return
        

@admin.register(UserSelectedDietPlan)
class UserSelectedDietPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'daily_calories', 'assigned_at')
    list_filter = ('assigned_at',)
    search_fields = ('user__username', 'user__email')