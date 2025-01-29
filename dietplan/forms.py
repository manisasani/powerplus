from django import forms
from accounts.models import Profile

class DietGoalForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['plan_goal']
        widgets = {
            'plan_goal': forms.RadioSelect()
        }
        labels = {
            'plan_goal': 'What is your goal?'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan_goal'].required = True