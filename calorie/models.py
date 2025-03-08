from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class FoodCategory(models.Model):
    """Model for categorizing food items"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Food Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    """Model for storing food items and their nutritional information"""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        FoodCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='foods'
    )
    # Basic nutritional information per 100g
    calories = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Calories per 100g'
    )
    protein = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Protein in grams per 100g'
    )
    carbs = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Carbohydrates in grams per 100g'
    )
    fat = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Fat in grams per 100g'
    )
    # Additional nutritional information (optional)
    fiber = models.FloatField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text='Fiber in grams per 100g'
    )
    sugar = models.FloatField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text='Sugar in grams per 100g'
    )
    # Serving information
    serving_size = models.FloatField(
        validators=[MinValueValidator(0)],
        default=100,
        help_text='Default serving size in grams'
    )
    common_serving = models.CharField(
        max_length=100,
        blank=True,
        help_text='Common serving description (e.g., "1 cup", "1 slice")'
    )
    # Meta information
    is_verified = models.BooleanField(
        default=False,
        help_text='Indicates if the nutritional information has been verified'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),  # For faster search
        ]

    def __str__(self):
        return self.name

class UserFoodLog(models.Model):
    """Model for tracking user's food consumption"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE
    )
    amount = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text='Amount in grams'
    )
    meal_type = models.CharField(
        max_length=20,
        choices=[
            ('breakfast', 'Breakfast'),
            ('lunch', 'Lunch'),
            ('dinner', 'Dinner'),
            ('snack', 'Snack'),
        ]
    )
    date = models.DateField()
    notes = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.food_item.name} - {self.date}"

    @property
    def calories_consumed(self):
        return (self.food_item.calories * self.amount) / 100

    @property
    def protein_consumed(self):
        return (self.food_item.protein * self.amount) / 100

    @property
    def carbs_consumed(self):
        return (self.food_item.carbs * self.amount) / 100

    @property
    def fat_consumed(self):
        return (self.food_item.fat * self.amount) / 100
    
class CustomFoodRequest(models.Model):
    """Model for users to request adding new food items"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User"
    )
    name = models.CharField(max_length=200, verbose_name="Food Name")
    description = models.TextField(blank=True, verbose_name="Description")
    suggested_category = models.ForeignKey(
        FoodCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Suggested Category"
    )
    # Suggested nutritional information
    calories = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Calories (per 100g)")
    protein = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Protein (per 100g)")
    carbs = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Carbohydrates (per 100g)")
    fat = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Fat (per 100g)")
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Request Status"
    )
    admin_notes = models.TextField(blank=True, verbose_name="Admin Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    def __str__(self):
        return f"{self.name} ({self.get_status_display()}) - Requested by {self.user.email}"
