from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUser(AbstractUser):
    GENDER = (("M", "Male"), ("F", "Female"))
    email = models.EmailField(unique=True)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    gender = models.CharField(max_length=1, choices=GENDER)
    height = models.IntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(300)]
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(500)]
    )


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )

    ACTIVITY_CHOICES = (
        ("very active", "Very Active"),
        ("active", "Active"),
        ("moderately active", "Moderately Active"),
        ("lightly active", "Lightly Active"),
    )
    EXPERIENCE_LEVEL = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("expert", "Expert"),
    )
    DIET_GOAL = (
        ("lose weight", "Lose Weight"),
        ("gain weight", "Gain Weight"),
        ("maintain weight", "Maintain Weight"),
        ("muscle_building", "Muscle Building"),
    )
    PLAN_GOAL = (
        ("muscle gain", "Muscle Gain"),
        ("fat loss", "Fat Loss"),
        ("fitness", "Fitness"),
    )
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL)
    diet_goal = models.CharField(max_length=20, choices=DIET_GOAL)
    plan_goal = models.CharField(max_length=20, choices=PLAN_GOAL)

    def __str__(self):
        return f"Profile of {self.user.username}"
