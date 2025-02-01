from django import forms
from accounts.models import DietPlanInfo

class DietGoalForm(forms.ModelForm):
    class Meta:
        model = DietPlanInfo
        fields = ['diet_goal']
        widgets = {
            'diet_goal': forms.RadioSelect()
        }
        labels = {
            'diet_goal': 'What is your goal?'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['diet_goal'].required = True

class ActivityLevelForm(forms.ModelForm):
    class Meta:
        model = DietPlanInfo
        fields = ['activity_level']
        widgets = {
            'activity_level': forms.RadioSelect()
        }
        labels = {
            'activity_level': 'What is your activity level?'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['activity_level'].required = True