from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class WorkoutPlan(models.Model):
    PLAN_GOAL = (
        ("muscle gain", "Muscle Gain"),
        ("fat loss", "Fat Loss"),
        ("fitness", "Fitness"),
    )
    EXPERIENCE_LEVEL = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("expert", "Expert"),
    )
    goal = models.CharField(max_length=30, choices=PLAN_GOAL)
    experience_level = models.CharField(max_length=30, choices=EXPERIENCE_LEVEL)
    sessions_per_week = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    rest_between_sets = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(180)],
        help_text="Rest time in seconds"
    )

    day1_title = models.CharField(max_length=60)
    day1_exercises = models.TextField()

    day2_title = models.CharField(max_length=60)
    day2_exercises = models.TextField()

    day3_title = models.CharField(max_length=60)
    day3_exercises = models.TextField()

    day4_title = models.CharField(max_length=60, null=True, blank=True)
    day4_exercises = models.TextField(null=True, blank=True)

    day5_title = models.CharField(max_length=60, null=True, blank=True)
    day5_exercises = models.TextField(null=True, blank=True)

    day6_title = models.CharField(max_length=60, null=True, blank=True)
    day6_exercises = models.TextField(null=True, blank=True)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.goal} plan for {self.experience_level}"

    class Meta:
        ordering = ['-created_at']


class UserSelectedWorkoutPlan(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='selected_workout_plan'
    )
    selected_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name='user_selections'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Workout plan for {self.user.username}"

    class Meta:
        ordering = ['-created_at']