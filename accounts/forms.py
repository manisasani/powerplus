from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser, Profile, DietPlanInfo, WorkoutPlanInfo
from django.core.validators import MinValueValidator, MaxValueValidator
from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        """
        # Ensure you call the parent class's save_user first!
        user = super().save_user(request, user, form, commit=False)

        # Get the data from the form:
        data = form.cleaned_data
        user.username = data.get("email")
        user.first_name = data.get("first_name")
        user.age = data.get("age")
        user.gender = data.get("gender")
        user.height = data.get("height")
        user.weight = data.get("weight")

        if commit:
            user.save()
        return user


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=50, required=True)
    age = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        label="age",
        required=True,
    )
    gender = forms.ChoiceField(choices=CustomUser.GENDER, label="gender", required=True)
    height = forms.IntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(300)],
        label="height (cm)",
        required=True,
    )
    weight = forms.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(500)],
        label="weight (kg)",
        required=True,
    )
    field_order = [
        "email",
        "first_name",
        "age",
        "gender",
        "height",
        "weight",
        "password1",
        "password2",
    ]

    def save(self, request):
        user = super().save(request)
        return user

