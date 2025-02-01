from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    GENDER = (("M", "Male"), ("F", "Female"))
    email = models.EmailField(unique=True)
    age = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
          null=False,
          blank=False
    )
    gender = models.CharField(
        max_length=1, 
        choices=GENDER,
        null=False,
        blank=False,
        )
    height = models.IntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(300)],
        null=False,
        blank=False,
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(500)],
        null=False,
        blank=False,
    )


class DietPlanInfo(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="diet_info"
    )
    DIET_GOAL = (
        ("lose weight", "Lose Weight"),
        ("gain weight", "Gain Weight"),
        ("maintain weight", "Maintain Weight"),
        ("muscle_building", "Muscle Building"),
    )
    ACTIVITY_CHOICES = (
        ("very active", "Very Active"),
        ("active", "Active"),
        ("moderately active", "Moderately Active"),
        ("lightly active", "Lightly Active"),
    )
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    diet_goal = models.CharField(max_length=20, choices=DIET_GOAL)

    def __str__(self):
        return f"Diet Info for {self.user.username}"
    

class WorkoutPlanInfo(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="workout_info"
    )
    EXPERIENCE_LEVEL = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("expert", "Expert"),
    )
    PLAN_GOAL = (
        ("muscle gain", "Muscle Gain"),
        ("fat loss", "Fat Loss"),
        ("fitness", "Fitness"),
    )
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL)
    plan_goal = models.CharField(max_length=20, choices=PLAN_GOAL)

    def __str__(self):
        return f"Workout Info for {self.user.username}"
    

class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name="main_profile"
    )
    data_diet = models.OneToOneField(
        DietPlanInfo, 
        on_delete=models.SET_NULL, 
        related_name="profile",
        null=True,
        blank=True
    )
    data_plan = models.OneToOneField(
        WorkoutPlanInfo, 
        on_delete=models.SET_NULL, 
        related_name="profile",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Profile of {self.user.username}"
    
@receiver(post_save, sender=CustomUser)
def create_user_profile_and_info(sender, instance, created, **kwargs):
    if created:
        # ایجاد Profile
        profile = Profile.objects.create(user=instance)
        
        # ایجاد DietPlanInfo
        diet_info = DietPlanInfo.objects.create(
            user=instance,
            activity_level="lightly active",
            diet_goal="maintain weight"
        )
        
        # ایجاد WorkoutPlanInfo
        workout_info = WorkoutPlanInfo.objects.create(
            user=instance,
            experience_level="beginner",
            plan_goal="fitness"
        )
        
        # ارتباط Profile با DietPlanInfo و WorkoutPlanInfo
        profile.data_diet = diet_info
        profile.data_plan = workout_info
        profile.save()

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'main_profile'):
        instance.main_profile.save()