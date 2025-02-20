from django.test import TestCase, Client
from .models import WorkoutPlan, UserSelectedWorkoutPlan
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()
class WorkoutplanModelTest(TestCase):
    def setUp(self):
        self.valid_plan = {
            'goal':'muscle gain',
            'experience_level': 'beginner',
            'sessions_per_week': 4,
            'rest_between_sets': 60,
            'day1_title':'test title',
            'day1_exercises': 'test exercises',
            'day2_title': 'test title2',
            'day2_exercises': 'test exercises2'
        }

    def test_create_valid_workout_plan(self):
        plan = WorkoutPlan.objects.create(**self.valid_plan)
        self.assertEqual(plan.goal, 'muscle gain')
        self.assertEqual(plan.experience_level, 'beginner')
        self.assertEqual(plan.sessions_per_week, 4)    
        self.assertEqual(plan.rest_between_sets, 60)          
        self.assertEqual(plan.day1_title, 'test title')     
        self.assertEqual(plan.day1_exercises, 'test exercises')
        self.assertEqual(plan.day2_title, 'test title2')     
        self.assertEqual(plan.day2_exercises, 'test exercises2')

    def test_invalid_sessions_per_week(self):
        invalid_plan = self.valid_plan.copy()
        invalid_plan['sessions_per_week'] = 10
        plan = WorkoutPlan.objects.create(**invalid_plan)
        with self.assertRaises(ValidationError):
            plan.full_clean()

    def test_invalid_rest_between_sets(self):
        invalid_plan = self.valid_plan.copy()
        invalid_plan['rest_between_sets'] = 190
        plan = WorkoutPlan.objects.create(**invalid_plan)
        with self.assertRaises(ValidationError):
            plan.full_clean()

    def test_invalid_goal(self):
        invalid_plan = self.valid_plan.copy()
        invalid_plan['goal'] = 'test'
        plan = WorkoutPlan.objects.create(**invalid_plan)
        with self.assertRaises(ValidationError):
            plan.full_clean()

    def test_invalid_experience_level(self):
        invalid_plan = self.valid_plan.copy()
        invalid_plan['experience_level'] = 'test'
        plan = WorkoutPlan.objects.create(**invalid_plan)
        with self.assertRaises(ValidationError):
            plan.full_clean()
    

    def test_optional_fields(self):
        plan = WorkoutPlan.objects.create(**self.valid_plan)
        
        plan.day3_title = 'Day3'
        plan.day3_exercises = 'test descripaiton'
        plan.save()
        plan.full_clean()

        plan.notes = 'Some important notes'
        plan.save()
        plan.full_clean()

    def test_string_representation(self):
        plan = WorkoutPlan.objects.create(**self.valid_plan)
        self.assertEqual(str(plan), "muscle gain plan for beginner")

    def test_ordering(self):
        first_plan = WorkoutPlan.objects.create(**self.valid_plan)
        second_plan = WorkoutPlan.objects.create(**self.valid_plan)

        plans = WorkoutPlan.objects.all()
        self.assertEqual(plans[0], second_plan)
        self.assertEqual(plans[1], first_plan)

class UserSelectedWorkoutplanTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testpass123',
            gender = 'M',
            age = 25,
            height=180,
            weight=80,
        )

        self.valid_plan = WorkoutPlan.objects.create(
            goal='muscle gain',
            experience_level='beginner',
            sessions_per_week=4,
            rest_between_sets=60,
            day1_title='test title',
            day1_exercises='test exercises',
            day2_title='test title2',
            day2_exercises='test exercises2',
        )

    def test_create_user_workout_plan(self):
        plan = UserSelectedWorkoutPlan.objects.create(
            user = self.user,
            selected_plan = self.valid_plan,
        )
        self.assertEqual(plan.user , self.user)
        self.assertEqual(plan.selected_plan, self.valid_plan)

    def test_unique_user_constraint(self):
        UserSelectedWorkoutPlan.objects.create(
            user = self.user,
            selected_plan = self.valid_plan,
        )
        with self.assertRaises(Exception):
            UserSelectedWorkoutPlan.objects.create(
                user = self.user,
                selected_plan = self.valid_plan,
            )
    def test_cascade_delet_user(self):
        plan = UserSelectedWorkoutPlan.objects.create(
            user = self.user,
            selected_plan = self.valid_plan
        )
        self.user.delete()
        with self.assertRaises(UserSelectedWorkoutPlan.DoesNotExist):
            UserSelectedWorkoutPlan.objects.get(pk=plan.pk)
    
    def test_cascade_delete_workout(self):
        plan = UserSelectedWorkoutPlan.objects.create(
            user = self.user,
            selected_plan = self.valid_plan,
        )
        self.valid_plan.delete()
        with self.assertRaises(UserSelectedWorkoutPlan.DoesNotExist):
            UserSelectedWorkoutPlan.objects.get(pk=plan.pk)

    def test_string_representations(self):
        plan = UserSelectedWorkoutPlan.objects.create(
            user = self.user,
            selected_plan = self.valid_plan,
        )
        self.assertEqual(str(plan), f"Workout plan for {self.user.username}")

    def test_ordering(self):
        first_plan = UserSelectedWorkoutPlan.objects.create(
            user = self.user,
            selected_plan = self.valid_plan,
        )

        second_user = User.objects.create_user(
            username='testuser2',
            email= ' test2@gmail.com',
            password='testpass123',
            gender='M',
            age=30,
            height=175,
            weight=75,
        )
        second_plan = UserSelectedWorkoutPlan.objects.create(
            user = second_user,
            selected_plan = self.valid_plan
        )
        plans = UserSelectedWorkoutPlan.objects.all()
        self.assertEqual(plans[0], second_plan)
        self.assertEqual(plans[1], first_plan)


class WorkoutplanViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testpass123',
            gender = 'M',
            age = 25,
            height=180,
            weight=80,
        )

        self.valid_plan = WorkoutPlan.objects.create(
            goal='muscle gain',
            experience_level='beginner',
            sessions_per_week=4,
            rest_between_sets=60,
            day1_title='test title',
            day1_exercises='test exercises',
            day2_title='test title2',
            day2_exercises='test exercises2',
        )
    def test_view_unauthorized(self):
        response = self.client.get(reverse('workoutplan:workoutplan'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/workoutplan/plan/')

    def test_view_authorized(self):
        self.client.login(
            username='testuser',
            password='testpass123'
        )
        response = self.client.get(reverse('pages:home'))
        self.assertEqual(response.status_code, 200)


    def test_existing_plan_display(self):

        user_plan = UserSelectedWorkoutPlan.objects.create(
            user=self.user,
            selected_plan=self.valid_plan,  
        )

        self.client.login(
            username='testuser',
            password='testpass123'
        )
        
        response = self.client.get(reverse('workoutplan:workoutplan'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('plan', response.context)
        self.assertEqual(response.context['plan'], self.valid_plan)
        self.assertEqual(response.context['current_sessions'], self.valid_plan.sessions_per_week)

    def test_create_new_plan(self):
        self.user.workout_info.plan_goal = 'muscle gain'
        self.user.workout_info.experience_level = 'beginner'
        self.user.workout_info.save()

        self.client.login(
            username='testuser',
            password='testpass123'
        )
        response = self.client.get(reverse('workoutplan:workoutplan'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserSelectedWorkoutPlan.objects.filter(user=self.user).exists())

    def test_no_suitable_plan(self):
        self.client.login(
            username='testuser',
            password='testpass123',
        )
        self.valid_plan.delete()
        response = self.client.get(reverse('workoutplan:workoutplan'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_change_sessions(self):
        self.user.workout_info.plan_goal = 'muscle gain'
        self.user.workout_info.experience_level = 'beginner'
        self.user.workout_info.save()

        intial_plan = UserSelectedWorkoutPlan.objects.create(
            user=self.user,
            selected_plan=self.valid_plan
        )
        self.client.login(
            username='testuser',
            password='testpass123'
        )

        response = self.client.post(reverse('workoutplan:change_sessions'), {'sessions': 4})
        self.assertEqual(response.status_code, 302)

        user_plan = UserSelectedWorkoutPlan.objects.get(user=self.user)
        self.assertEqual(user_plan.selected_plan.sessions_per_week, 4)

    def test_update_plan(self):
        user_plan =UserSelectedWorkoutPlan.objects.create(
            user=self.user,
            selected_plan = self.valid_plan
        )
        self.client.login(
            username='testuser',
            password='testpass123'
        )
        response = self.client.post(reverse('workoutplan:update'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(UserSelectedWorkoutPlan.objects.filter(user=self.user).exists())

    def test_download_pdf(self):
        user_paln = UserSelectedWorkoutPlan.objects.create(
            user=self.user,
            selected_plan=self.valid_plan
        )
        self.client.login(
            username='testuser',
            password='testpass123'
        )
        response = self.client.get(reverse('workoutplan:download_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-type'], 'application/pdf')

    def test_download_pdf_no_plan(self):
        self.client.login(
            username='testuser',
            password='testpass123',
        )
        response = self.client.get(reverse('workoutplan:download_pdf'))
        self.assertEqual(response.status_code, 302)

    def test_goal_form_submission(self):
        self.client.login(
            username='testuser',
            password='testpass123',
        )
        response = self.client.post(reverse('workoutplan:goal'),{
            'plan_goal': 'muscle gain'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.workout_info.plan_goal, 'muscle gain')


    def test_experience_form_submission(self):
        self.client.login(
            usrname='testuser',
            password='testpass123'
        )
        response = self.client.post(reverse('workoutplan:goal'), {
            'experience_level': 'beginner'
        })

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.workout_info.experience_level, 'beginner')

    def test_invalid_session_change(self):
        
        self.user.workout_info.plan_goal = 'muscle gain'
        self.user.workout_info.experience_level = 'beginner'
        self.user.workout_info.save()

        
        initial_plan = UserSelectedWorkoutPlan.objects.create(
            user=self.user,
            selected_plan=self.valid_plan
        )

        self.client.login(
            username='testuser',
            password='testpass123'
        )

    
        response = self.client.post(reverse('workoutplan:change_sessions'), {
            'sessions': 10 
        })

        
        self.assertEqual(response.status_code, 302)  

        user_plan = UserSelectedWorkoutPlan.objects.get(user=self.user)
        self.assertEqual(user_plan.selected_plan.sessions_per_week, 4)

    def test_unauthorized_form_access(self):
        response = self.client.get(reverse('workoutplan:goal'))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(reverse('workoutplan:experience'))
        self.assertEqual(response.status_code, 302)
