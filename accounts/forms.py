from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser, Profile
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomSignupForm(SignupForm):
    firstname = forms.CharField(max_length=50)
    age = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)], label="age"
    )
    gender = forms.ChoiceField(choices=CustomUser.GENDER, label="gender")
    height = forms.IntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(300)],
        label="height (cm)",
    )
    weight = forms.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(500)],
        label="weight (kg)",
    )

    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data["name"]
        user.age = self.cleaned_data["age"]
        user.gender = self.cleaned_data["gender"]
        user.height = self.cleaned_data["height"]
        user.weight = self.cleaned_data["weight"]
        user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("activity_level", "experience_level", "diet_goal", "plan_goal")
