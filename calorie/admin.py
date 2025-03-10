from django.contrib import admin
from .models import FoodCategory, FoodItem, UserFoodLog, CustomFoodRequest
@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'calories', 'protein', 'carbs', 'fat'] 
    list_filter = ['category']
    search_fields = ['name']
    list_per_page = 20

@admin.register(UserFoodLog)  
class UserFoodLogAdmin(admin.ModelAdmin):  
    list_display = ['user', 'food_item', 'amount', 'meal_type', 'date']
    list_filter = ['date', 'meal_type', 'user']
    search_fields = ['user__email', 'food_item__name']

@admin.register(CustomFoodRequest)
class CustomFoodRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'user__email']