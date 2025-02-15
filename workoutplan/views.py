from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from django.contrib import messages
from accounts.models import WorkoutPlanInfo
from .models import WorkoutPlan, UserSelectedWorkoutPlan
from .forms import WorkoutGoalForm, ExperienceLevelForm
from django.urls import reverse_lazy
from django.views.generic import View
from django.utils import timezone
from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa

class WorkoutGoalView(LoginRequiredMixin, UpdateView):
    model = WorkoutPlanInfo
    form_class = WorkoutGoalForm
    template_name = 'plan_goal.html'
    success_url = reverse_lazy('workoutplan:experience')

    def get(self, request, *args, **kwargs):
        existing_plan = UserSelectedWorkoutPlan.objects.filter(user=request.user).first()
        if existing_plan:
            return redirect('workoutplan:workoutplan')
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        plan_info, created = WorkoutPlanInfo.objects.get_or_create(
            user=self.request.user,
            defaults={
                'experience_level': 'beginner',
                'plan_goal': 'muscle gain'
            }
        )
        return plan_info

    def form_valid(self, form):
        messages.success(self.request, 'Your workout goal has been set!')
        return super().form_valid(form)

class ExperienceLevelView(LoginRequiredMixin, UpdateView):
    model = WorkoutPlanInfo
    form_class = ExperienceLevelForm
    template_name = 'plan_experience.html'
    success_url = reverse_lazy('workoutplan:workoutplan')

    def get(self, request, *args, **kwargs):
        if not request.user.workout_info.plan_goal:
            return redirect('workoutplan:goal')
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        plan_info, created = WorkoutPlanInfo.objects.get_or_create(
            user=self.request.user,
            defaults={
                'experience_level': 'beginner',
                'plan_goal': 'muscle gain'
            }
        )
        return plan_info

    def form_valid(self, form):
        messages.success(self.request, 'Your experience level has been set!')
        return super().form_valid(form)
    
class WorkoutPlanView(LoginRequiredMixin, DetailView):
    template_name = 'plan.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user

        available_plans = WorkoutPlan.objects.filter(
            goal = user.workout_info.plan_goal,
            experience_level = user.workout_info.experience_level
        ).order_by('sessions_per_week')

        existing_plan = UserSelectedWorkoutPlan.objects.filter(user=user).first()

        if not existing_plan:
            if not available_plans.exists():
                context = {
                    'user':user,
                    'plan':None,
                    'error': 'NO suitable workout plan found for your goals and experience level.'
                }
                return render(request, self.template_name, context)
            
            workout_plan =available_plans.first()
            existing_plan = UserSelectedWorkoutPlan.objects.create(
                user=user,
                selected_plan=workout_plan,
            )
        context = {
            'user':user,
            'plan':existing_plan.selected_plan,
            'available_plans': available_plans,
            'current_sessions': existing_plan.selected_plan.sessions_per_week
        }
        return render(request, self.template_name, context)
    
class ChangePlanSessionView(LoginRequiredMixin, View):
    def post(self, request):
        sessions = request.POST.get('sessions')

        if not sessions:
            return redirect('workoutplan:workoutplan')

        user = request.user

        new_plan = WorkoutPlan.objects.filter(
            goal=user.workout_info.plan_goal,
            experience_level=user.workout_info.experience_level,
            sessions_per_week=sessions
        ).first()

        if new_plan:
            UserSelectedWorkoutPlan.objects.update_or_create(
                user=user,
                defaults={'selected_plan': new_plan}
            )

        return redirect('workoutplan:workoutplan')
    
class UpdateWorkoutPlanView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        UserSelectedWorkoutPlan.objects.filter(user=self.request.user).delete()
        return redirect('workoutplan:goal')
    
class DownloadWorkoutPlanPDF(LoginRequiredMixin, View):
    def get(self, request):
        user_plan = UserSelectedWorkoutPlan.objects.filter(user=request.user).first()
        if not user_plan:
            messages.error(request, 'No workout plan found. Please create a plan first.')
            return redirect('workoutplan:workoutplan')
        
    
        workout_plan = user_plan.selected_plan
        
        context = {
            'user_info': request.user,
            'plan': workout_plan, 
            'current_date': timezone.now().strftime('%Y-%m-%d')
        }
        template = get_template('pdfplan_template.html')
        html = template.render(context)

        try:
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
            if not pdf.err:
                filename = f"workout_plan-{request.user.username}-{timezone.now().strftime('%Y%m%d')}.pdf"
                response = HttpResponse(result.getvalue(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            else:
                messages.error(request, 'Error generating PDF')
        except Exception as e:
            messages.error(request, f'Error generating PDF: {str(e)}')
        
        return redirect('workoutplan:workoutplan')