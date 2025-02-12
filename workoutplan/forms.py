from django import forms 
from accounts.models import WorkoutPlanInfo

class WorkoutGoalForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlanInfo
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


class ExperienceLevelForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlanInfo
        fields = ['experience_level']
        widgets = {
            'experience_level': forms.RadioSelect()
        }
        labels = {
            'experience_level': 'What is your experience?'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['experience_level'].required = True