from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import DietPlan, UserSelectedDietPlan
from accounts.models import DietPlanInfo
from django.core.exceptions import ValidationError
from .forms import DietGoalForm  , ActivityLevelForm 

User = get_user_model()
class DietPlanModelTests(TestCase):
    def setUp(self):
        self.valid_plan = {
            'goal': 'lose weight',
            'calorie_range_min': 1500,
            'calorie_range_max':2000,
            'protein_percentage':30,
            'carbs_percentage':50,
            'fat_percentage':20,
            'breakfast': 'Test breakfast',
            'lunch': 'Test lunch',
            'dinner': 'Test dinnder',
        }
    
    def test_create_valid_diet_plan(self):
        plan = DietPlan.objects.create(**self.valid_plan)
        self.assertEqual(plan.goal, 'lose weight')
        self.assertEqual(plan.calorie_range_min, 1500)

    def test_invalid_macros_total(self):
        invalid_plan = self.valid_plan.copy()
        invalid_plan['protein_percentage'] = 40
        with self.assertRaises(ValidationError):
            DietPlan.objects.create(**invalid_plan)

    def test_invalid_fat_percentage(self):
        invalid_plan = self.valid_plan.copy()
        invalid_plan['fat_percentage'] = 15
        with self.assertRaises(ValidationError):
            DietPlan.objects.create(**invalid_plan)

    def test_str_respresentations(self):
        plan = DietPlan.objects.create(**self.valid_plan)
        expected = f"Diet plan for lose weight (1500-2000 cal)"
        self.assertEqual(str(plan), expected)

class UserSelectedDietPlanTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email = 'Test@gmail.com',
            password = 'Test1234@',
            gender = 'M',
            age = 25,
            height = 180,
            weight = 80

        )
        self.diet_plan = DietPlan.objects.create(
            goal = 'lose weight',
            calorie_range_min = 1500,
            calorie_range_max = 2000,
            protein_percentage= 30,
            carbs_percentage= 50,
            fat_percentage=20,
        )
    def test_create_user_diet_plan(self):
        plan = UserSelectedDietPlan.objects.create(
            user = self.user,
            selected_plan = self.diet_plan,
            daily_calories = 1000
        )
        self.assertEqual(plan.user, self.user)
        self.assertEqual(plan.daily_calories, 1000)

    def test_unique_user_constraint(self):
        UserSelectedDietPlan.objects.create(
            user=self.user,
            selected_plan = self.diet_plan,
            daily_calories= 1000
        )
        with self.assertRaises(Exception):
            UserSelectedDietPlan.objects.create(
                user=self.user,
                selected_plan = self.diet_plan,
                daily_calories = 2000
            )

class DietPlanViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser4',
            email='test@gmail.com',
            password='testpass123',
            gender='M',
            age=25,
            height=180,
            weight=80,
        )
        self.diet_info = DietPlanInfo.objects.get(user=self.user)
        self.diet_info.activity_level = 'moderately active'
        self.diet_info.diet_goal = 'lose weight'
        self.diet_info.save()
        
        self.diet_plan = DietPlan.objects.create(
            goal= 'lose weight',
            calorie_range_min = 1500,
            calorie_range_max = 2500,
            protein_percentage= 30,
            carbs_percentage = 50,
            fat_percentage = 20,
        )

    def test_activity_level_view_unauthorized(self):
        response = self.client.get(reverse('dietplan:activity'))
        self.assertEqual(response.status_code, 302)

    def test_activity_level_view_authorized(self):
        self.client.login(username='testuser4', password='testpass123')
        response = self.client.get(reverse('dietplan:activity'))
        self.assertEqual(response.status_code , 200)

    def test_diet_plan_view_calculations(self):
        self.client.login(username='testuser4', password='testpass123')
        response = self.client.get(reverse('dietplan:plan'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('daily_calories', response.context)
        self.assertIn('macros', response.context)

    def test_update_diet_plan(self):
        self.client.login(username='testuser4', password='testpass123')
        UserSelectedDietPlan.objects.create(
            user=self.user,
            selected_plan=self.diet_plan,
            daily_calories=2000
        )
        response = self.client.post(reverse('dietplan:update_plan'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserSelectedDietPlan.objects.filter(user=self.user).count(), 0)

    def test_invalid_calorie_range(self):
        self.diet_plan.calorie_range_max = 1000
        with self.assertRaises(ValidationError):
            self.diet_plan.full_clean()  
            self.diet_plan.save()

class DietPlanFormTest(TestCase):
    
    def setUp(self):
        self.user= User.objects.create_user(
            username='testuser5',
            email='testtuser@gmail.com',
            password='passtest333',
            gender = 'M',
            age= 23,
            height=180,
            weight=80,

        )
        self.diet_info = DietPlanInfo.objects.get(user=self.user)
        
    def test_diet_goal_form_valid(self):
        form_data = {'diet_goal': 'lose weight'}
        form = DietGoalForm(
            data=form_data,
            instance = self.diet_info
        )
        self.assertTrue(form.is_valid())

    def test_acticity_level_form_valid(self):
        form_data  ={'activity_level': 'moderately active'}
        form = ActivityLevelForm(
            data = form_data,
            instance = self.diet_info
        )
        self.assertTrue(form.is_valid())

    def test_forms_required_fields(self):
        form1 = DietGoalForm(data={})
        form2 = ActivityLevelForm(data={})
        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())

class DietPlanViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser4',
            email='test@gmail.com',
            password='testpass123',
            gender='M',
            age=25,
            height=180,
            weight=80,
        )
        self.diet_plan = DietPlan.objects.create(
            goal= 'lose weight',
            calorie_range_min = 1500,
            calorie_range_max = 2500,
            protein_percentage= 30,
            carbs_percentage = 50,
            fat_percentage = 20,
        )

        self.diet_info = DietPlanInfo.objects.get(user=self.user)
        self.diet_info.activity_level = 'moderately active'
        self.diet_info.diet_goal = 'lose weight'
        self.diet_info.save()

    def test_bmr_caclulation(self):
        self.client.login(
        username = 'testuser4',
        password = 'testpass123'
        )
        response = self.client.get(reverse('dietplan:plan'))
        self.assertIn('daily_calories', response.context)

    def test_on_suitable_plan(self):
        self.client.login(
            username= 'testuser4',
            password= 'testpass123'
        )
        self.diet_info.diet_goal = 'gainweight'
        self.diet_info.save()
        response = self.client.get(reverse('dietplan:plan'))
        self.assertIn('error', response.context)

    def test_download_pdf_unauthorized(self):
        self.client.login(
            username = 'testuser4',
            password = 'testpass123'
        )
        response = self.client.get(reverse('dietplan:download_pdf'))
        self.assertEqual(response.status_code, 302)

    def test_download_pdf_with_plan(self):
        self.client.login(
            username = 'testuser4',
            password = 'testpass123'
        )
        UserSelectedDietPlan.objects.create(
            user = self.user,
            selected_plan = self.diet_plan,
            daily_calories = 2000
        )
        response = self.client.get(reverse('dietplan:download_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')