from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from accounts.models import Profile
from .forms import DietGoalForm
class DietGoalView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = DietGoalForm
    template_name = 'diet_goal.html'
    success_url = reverse_lazy('dietplan')