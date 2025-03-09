from django import forms
from .models import UserFoodLog, FoodItem, FoodCategory

class FoodSearchForm(forms.Form):
    query = forms.CharField(
        label='Search Foods',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter food name...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=FoodCategory.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class FoodLogForm(forms.ModelForm):
    class Meta:
        model = UserFoodLog
        fields = ['food_item', 'amount', 'meal_type', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.1'
            }),
            'meal_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }