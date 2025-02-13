from django.contrib import admin
from .models import WorkoutPlan, UserSelectedWorkoutPlan
from django.core.exceptions import ValidationError

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('goal', 'experience_level', 'sessions_per_week', 'created_at')
    list_filter = ('goal', 'experience_level', 'sessions_per_week')
    search_fields = ('goal', 'notes', 'day1_title', 'day2_title', 'day3_title')

    fieldsets = (
        ('Basic Information', {
            'fields': ('goal', 'experience_level', 'sessions_per_week', 'rest_between_sets')
        }),
        ('Day 1', {
            'fields': ('day1_title', 'day1_exercises')
        }),
        ('Day 2', {
            'fields': ('day2_title', 'day2_exercises')
        }),
        ('Day 3', {
            'fields': ('day3_title', 'day3_exercises')
        }),
        ('Additional Days', {
            'classes': ('collapse',), 
            'fields': (
                'day4_title', 'day4_exercises',
                'day5_title', 'day5_exercises',
                'day6_title', 'day6_exercises'
            )
        }),
        ('Additional Information', {
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

@admin.register(UserSelectedWorkoutPlan)
class UserSelectedWorkoutPlanAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'get_goal', 'get_experience', 'created_at')

    list_filter = ('created_at', 'selected_plan__goal', 'selected_plan__experience_level')

    search_fields = ('user__username', 'user__email')

    readonly_fields = ('created_at',)

    def get_goal(self, obj):
        return obj.selected_plan.goal
    get_goal.short_description = 'Goal' 

    def get_experience(self, obj):
        return obj.selected_plan.experience_level
    get_experience.short_description = 'Experience Level'