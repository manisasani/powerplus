from django.db import models
from accounts.models import Profile
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser,DietPlanInfo,WorkoutPlanInfo
class DietPlan(models.Model):
    DIET_GOAL = (
        ("lose weight", "Lose Weight"),
        ("gain weight", "Gain Weight"),
        ("maintain weight", "Maintain Weight"),
        ("muscle_building", "Muscle Building"),
    )
    goal = models.CharField(max_length=20, choices=DIET_GOAL)
    calorie_range_min = models.IntegerField(default=0)
    calorie_range_max = models.IntegerField(default=0)
    breakfast = models.TextField(default="")
    lunch = models.TextField(default="")
    dinner = models.TextField(default="")
    snacks = models.TextField(default="")
    snacks2 = models.TextField(default="")
    snacks3 = models.TextField(default="")
    protein_percentage = models.IntegerField(default=0)
    carbs_percentage = models.IntegerField(default=0)
    fat_percentage = models.IntegerField(default=0)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def validate_macros(self):
        total = self.protein_percentage + self.carbs_percentage + self.fat_percentage
        if total !=100:
            return False, f"The set of percentage macros must be equal to 100. The current value: {total}"   

        if self.fat_percentage < 20:
            return False, f"The fat percentage should not be less than 20."
        
        return True, "OK"
    
    def validate_calories(self):
        if self.calorie_range_max <= self.calorie_range_min:
            return False, "Maximum calories must be greater than minimum calories"
        return True, "OK"
    
    def save(self, *args, **kwargs):
        is_valid, message = self.validate_macros()
        if not is_valid:
            raise ValidationError(message)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['goal', 'calorie_range_min']
        verbose_name = 'Diet Plan'
        verbose_name_plural = 'Diet Plans'

    def __str__(self):
        return f"Diet plan for {self.goal} ({self.calorie_range_min}-{self.calorie_range_max} cal)"
    


class UserSelectedDietPlan(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='selected_diet')
    selected_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE)
    daily_calories = models.IntegerField()
    assigned_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}'s diet plan - {self.daily_calories} calories"

    class Meta:
        verbose_name = 'User Selected Diet Plan'
        verbose_name_plural = 'User Selected Diet Plans'
