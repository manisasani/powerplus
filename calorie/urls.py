from django.urls import path
from . import views

app_name = 'calorie'

urlpatterns = [
    path('foods/', views.food_list, name='food_list'),
    path('food/<int:pk>/', views.food_detail, name='food_detail'),
    path('summary/', views.daily_summary, name='daily_summary'),
]