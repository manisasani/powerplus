# calorie/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import FoodCategory, FoodItem, UserFoodLog
from .forms import FoodSearchForm, FoodLogForm

@login_required
def food_list(request):
    form = FoodSearchForm(request.GET)
    foods = FoodItem.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        
        if query:
            foods = foods.filter(name__icontains=query)
        if category:
            foods = foods.filter(category=category)
    
    context = {
        'form': form,
        'foods': foods,
        'categories': FoodCategory.objects.all()
    }
    return render(request, 'calorie/food_list.html', context)

@login_required
def food_detail(request, pk):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodLogForm(request.POST)
        if form.is_valid():
            food_log = form.save(commit=False)
            food_log.user = request.user
            food_log.food_item = food
            food_log.save()
            messages.success(request, 'Food logged successfully!')
            return redirect('calorie:daily_summary')
    else:
        form = FoodLogForm(initial={
            'food_item': food,
            'date': timezone.now().date()
        })
    
    context = {
        'food': food,
        'form': form
    }
    return render(request, 'calorie/food_detail.html', context)

@login_required
def daily_summary(request):
    date = request.GET.get('date', timezone.now().date())
    logs = UserFoodLog.objects.filter(
        user=request.user,
        date=date
    ).select_related('food_item')
    
    totals = {
        'calories': sum(log.calories_consumed for log in logs),
        'protein': sum(log.protein_consumed for log in logs),
        'carbs': sum(log.carbs_consumed for log in logs),
        'fat': sum(log.fat_consumed for log in logs)
    }
    
    meals = {
        'breakfast': logs.filter(meal_type='breakfast'),
        'lunch': logs.filter(meal_type='lunch'),
        'dinner': logs.filter(meal_type='dinner'),
        'snack': logs.filter(meal_type='snack')
    }
    
    context = {
        'date': date,
        'totals': totals,
        'meals': meals
    }
    return render(request, 'calorie/daily_summary.html', context)