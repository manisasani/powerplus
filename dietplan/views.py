from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import View
from django.urls import reverse_lazy
from accounts.models import DietPlanInfo
from django.views.generic import DetailView
from .forms import DietGoalForm, ActivityLevelForm
from .models import DietPlan, UserSelectedDietPlan
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa

class ActivityLevelView(LoginRequiredMixin, UpdateView):
    model = DietPlanInfo
    form_class = ActivityLevelForm
    template_name = "activity_level.html"
    success_url = reverse_lazy('dietplan:goal')
    def get(self, request, *args , **kwargs):
        existing_plan = UserSelectedDietPlan.objects.filter(user=request.user).first()
        if existing_plan:
            return redirect('dietplan:plan')
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        diet_info, created = DietPlanInfo.objects.get_or_create(
            user=self.request.user,
            defaults={
                'activity_level': 'lightly active',
                'diet_goal': 'maintain weight'
            }
        )  
        return self.request.user.diet_info
class DietGoalView(LoginRequiredMixin, UpdateView):
    model = DietPlanInfo
    form_class = DietGoalForm
    template_name = 'diet_goal.html'
    success_url = reverse_lazy('dietplan:plan')

    def get_object(self, queryset=None):
        diet_info, created = DietPlanInfo.objects.get_or_create(
            user=self.request.user,
            defaults={
                'activity_level': 'lightly active',
                'diet_goal': 'maintain weight'
            }
        )  
        return self.request.user.diet_info

class DietPlanView(LoginRequiredMixin, DetailView):
    template_name = "diet_plan.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user

        existing_plan = UserSelectedDietPlan.objects.filter(user=request.user).first()
        if existing_plan:
            daily_calories = existing_plan.daily_calories
            diet_plan = existing_plan.selected_plan

            protein_grams = (daily_calories * diet_plan.protein_percentage / 100) / 4
            carbs_grams = (daily_calories * diet_plan.carbs_percentage / 100) / 4
            fats_grams = (daily_calories * diet_plan.fat_percentage / 100) / 9

            context = {
                "user_info": user,
                "daily_calories": daily_calories,
                "diet_plan": diet_plan,
                "macros": {
                    "protein": int(protein_grams),
                    "carbs": int(carbs_grams),
                    "fats": int(fats_grams),
                },
                "has_existing_plan": True 
            }
            return render(request, self.template_name, context)
        
        # محاسبه BMR
        bmr = 10 * user.weight + 6.25 * user.height - 5 * user.age
        if user.gender == 'M':
            bmr += 5
        else:
            bmr -= 161

        # ضرایب فعالیت
        activity_multipliers = {
            'very active': 1.725,
            'active': 1.55,
            'moderately active': 1.375,
            'lightly active': 1.2
        }
        
        daily_calories = bmr * activity_multipliers[user.diet_info.activity_level]

        # لاگ اطلاعات پایه
        print(f"User Info:")
        print(f"- Weight: {user.weight}kg")
        print(f"- Height: {user.height}cm")
        print(f"- Age: {user.age}")
        print(f"- Gender: {user.gender}")
        print(f"- Activity Level: {user.diet_info.activity_level}")
        print(f"- BMR: {bmr:.2f}")
        print(f"- Daily Calories: {daily_calories:.2f}")

        # پیدا کردن برنامه غذایی مناسب
        diet_plan = DietPlan.objects.filter(
            goal=user.diet_info.diet_goal,
            calorie_range_min__lte=daily_calories,
            calorie_range_max__gte=daily_calories,
        ).first()

        if not diet_plan:
            context = {
                "user_info": user,
                "daily_calories": int(daily_calories),
                "diet_plan": None,
                "error": "هیچ برنامه غذایی مناسب پیدا نشد.",
            }
            return render(request, self.template_name, context)
        if diet_plan:
            # محاسبه ماکروها
            protein_grams = (daily_calories * diet_plan.protein_percentage / 100) / 4
            carbs_grams = (daily_calories * diet_plan.carbs_percentage / 100) / 4
            fats_grams = (daily_calories * diet_plan.fat_percentage / 100) / 9

            UserSelectedDietPlan.objects.create(
                user=user,
                selected_plan = diet_plan,
                daily_calories = int(daily_calories)
            )
            context = {
                'user_info': user,
                'diet_plan': diet_plan,
                'daily_calories': int(daily_calories),
                'macros': {
                'protein': int(protein_grams),
                'carbs': int(carbs_grams),
                'fats': int(fats_grams),
                },
                'has_existing_plan': True 
            }
            return render(request, self.template_name, context)

        # لاگ اطلاعات ماکروها
        print(f"\nMacronutrient Calculations:")
        print(f"Diet Plan: {diet_plan}")
        print(
            f"- Protein: {diet_plan.protein_percentage}% = {protein_grams:.1f}g ({protein_grams * 4:.0f} kcal)"
        )
        print(
            f"- Carbs: {diet_plan.carbs_percentage}% = {carbs_grams:.1f}g ({carbs_grams * 4:.0f} kcal)"
        )
        print(
            f"- Fats: {diet_plan.fat_percentage}% = {fats_grams:.1f}g ({fats_grams * 9:.0f} kcal)"
        )

        # بررسی نسبت پروتئین به وزن بدن
        protein_per_kg = protein_grams / user.weight
        print(f"\nProtein per kg of body weight: {protein_per_kg:.2f}g/kg")
        if protein_per_kg < 1.6 or protein_per_kg > 2.2:
            print("Warning: Protein intake is outside recommended range (1.6-2.2g/kg)")

        # بررسی مجموع کالری‌ها
        total_calories = (protein_grams * 4) + (carbs_grams * 4) + (fats_grams * 9)
        print(f"\nTotal calories from macros: {total_calories:.0f}")
        print(f"Difference from target: {daily_calories - total_calories:.0f} kcal")

        context = {
            "user_info": user,
            "daily_calories": int(daily_calories),
            "diet_plan": diet_plan,
            "macros": {
                "protein": int(protein_grams),
                "carbs": int(carbs_grams),
                "fats": int(fats_grams),
            },
        }
        return render(request, self.template_name, context)
    

class UpdateDietPlanView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        UserSelectedDietPlan.objects.filter(user=request.user).delete()
        return redirect('dietplan:activity')
    

class DownloadDietPlanPDF(LoginRequiredMixin, View):
    def get (self, request):
        user_plan  = UserSelectedDietPlan.objects.filter(user=request.user).first()
        if not user_plan:
            return redirect('dietplan:plan')
        
        context={
            'user_info': request.user,
            'daily_calories': user_plan.daily_calories,
            'diet_plan': user_plan.selected_plan,
            'macros':{
                'protein': int((user_plan.daily_calories * user_plan.selected_plan.protein_percentage / 100) / 4),
                'carbs': int((user_plan.daily_calories * user_plan.selected_plan.carbs_percentage / 100) / 4),
                'fats': int((user_plan.daily_calories * user_plan.selected_plan.fat_percentage / 100) / 9),
            },
            'current_date': timezone.now().strftime('%Y-%m-%d')


        }
        template = get_template('pdf_template.html')
        html = template.render(context)

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)

        if not pdf.err:
            filename = f"diet_plan-{request.user.email}-{timezone.now().strftime('%Y%m%d')}.pdf"
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        return HttpResponse('Error generating PDF', status=500)