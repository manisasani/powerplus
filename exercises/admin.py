from django.contrib import admin
from .models import Muscle, Exercise

@admin.register(Muscle)
class MuscleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'create_at']
    search_fields = ['name', 'description']
    list_filter = ['create_at']
    readonly_fields = ['create_at']

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'muscle', 'tags', 'create_at']
    search_fields = ['name', 'description', 'tags']
    list_filter = ['muscle', 'create_at']
    readonly_fields = ['create_at']
    autocomplete_fields = ['muscle'] 