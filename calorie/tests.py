from datetime import timedelta
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from .models import (
    FoodCategory, 
    FoodItem, 
    UserFoodLog,
    CustomFoodRequest
)

User = get_user_model()
class FoodCategoryModelTest(TestCase):
    def setUp(self):
        self.category = {
            'name': 'testname',
            'description' : 'test description',
        }
    def test_create_category(self):
        category = FoodCategory.objects.create(**self.category)
        self.assertEqual(category.name, 'testname')
        self.assertEqual(category.description, 'test description')

    def test_str_food_category(self):
        category = FoodCategory.objects.create(**self.category)
        self.assertEqual(category.__str__(), 'testname')

    def test_respect_ordering(self):
        FoodCategory.objects.create(name='name2', description='ds2', pk=2)
        FoodCategory.objects.create(name='name1', description='ds1', pk=1)
        results = FoodCategory.objects.all()
        self.assertEqual('name1', results[0].name)
        self.assertEqual('name2', results[1].name)

class FoodItemModelTest(TestCase):
    def setUp(self):
        self.category = FoodCategory.objects.create(
            name='testcategory', 
            description='test',
        )
        self.fooditem = {
            'name': 'food',
            'category': self.category,
            'calories' : 250, 
            'protein' : 45,    
            'carbs' : 55,      
            'fat' : 20,        
            'fiber' : 40, 
        }

    def test_create_fooditem(self):
        fooditem  = FoodItem.objects.create(**self.fooditem)
        self.assertEqual(fooditem.name, 'food')
        self.assertEqual(fooditem.category.name, 'testcategory')
        self.assertEqual(fooditem.protein, 45)

    def test_negative_values(self):
        with self.assertRaises(ValidationError):
            fooditem = FoodItem.objects.create(
                name='test',
                category=self.category,
                calories=-1,
                protein=45,
                carbs=55,
                fat=20
            )
            fooditem.full_clean()

    def test_str_food_item(self):
        item = FoodItem.objects.create(**self.fooditem)
        self.assertEqual(str(item), 'food')

class UserFoodLogModelTest(TestCase):
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
        self.category = FoodCategory.objects.create(
            name='testcategory', 
            description='test',
        )
        self.item = FoodItem.objects.create(
            name='food',
            category=self.category,
            calories=250,
            protein=45,
            carbs=55,
            fat=20,
            fiber=40, 
        )
        self.foodlog = {
            'user' : self.user,
            'food_item' : self.item
        }
    
    def test_create_food_log(self):
        from django.utils import timezone
        foodlog = UserFoodLog.objects.create(
            user = self.user,
            food_item = self.item,
            amount = 2,
            meal_type = 'breakfast',
            date=timezone.now().date()
        )
        self.assertEqual(foodlog.user, self.user)
        self.assertEqual(foodlog.food_item, self.item)
        self.assertEqual(foodlog.amount , 2)

    def test_str_food_log(self):
        from django.utils import timezone
        date = timezone.now().date()
        foodlog = UserFoodLog.objects.create(
            user = self.user,
            food_item = self.item,
            amount = 2,
            meal_type = 'breakfast',
            date=date
        )
        expected_str = f"{self.user.email} - {self.item.name} - {date}"
        self.assertEqual(str(foodlog), expected_str)

class FoodListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user= User.objects.create_user(
            username='testuser5',
            email='testtuser@gmail.com',
            password='passtest333',
            gender = 'M',
            age= 23,
            height=180,
            weight=80,
        )
    def test_food_list_view_unauthorized(self):
        response = self.client.get(reverse('calorie:food_list'))
        self.assertEqual(response.status_code, 302)

    def test_food_list_view_authorized(self):
        self.client.login(username='testuser5', password='passtest333')
        response = self.client.get(reverse('calorie:food_list'))
        self.assertEqual(response.status_code , 200)

    def test_empty_query_search(self):
        self.client.login(username='testuser5', password='passtest333')

        category1 = FoodCategory.objects.create(name='category 1 ', )
        food1 = FoodItem.objects.create(
            name='Apple',
            category=category1,
            calories=52,
            protein=0.3,
            carbs=14,
            fat=0.2,
        )
        food2 = FoodItem.objects.create(
            name='Banana',
            category = category1,
            calories = 89,
            protein=1.1,
            carbs=23,
            fat=0.3
        )
        response = self.client.get(reverse('calorie:food_list'))
        self.assertEqual(response.status_code , 200)
        self.assertTemplateUsed(response, 'calorie/food_list.html')
        self.assertContains(response, 'Apple')
        self.assertContains(response, 'Banana')

    def test_name_search(self):
        self.client.login(username='testuser5', password='passtest333')

        category1 = FoodCategory.objects.create(name='category1')
        food1 = FoodItem.objects.create(
            name='Apple',
            category=category1,
            calories=52,
            protein=0.3,
            carbs=14,
            fat=0.2,
        )
        food2 = FoodItem.objects.create(
            name='Banana',
            category = category1,
            calories = 89,
            protein=1.1,
            carbs=23,
            fat=0.3
        )

        response = self.client.get(f"{reverse('calorie:food_list')}?query=Apple")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calorie/food_list.html')
        self.assertContains(response, 'Apple')
        self.assertNotContains(response, 'Banana')
        self.assertEqual(len(response.context['foods']), 1)


    def test_category_filter(self):
        self.client.login(username='testuser5', password='passtest333')
         
        category1 = FoodCategory.objects.create(name='Fruits')
        category2 = FoodCategory.objects.create(name='Vegetables')
        
        food1 = FoodItem.objects.create(
            name='Apple',
            category=category1,
            calories=52,
            protein=0.3,
            carbs=14,
            fat=0.2
        )
        food2 = FoodItem.objects.create(
            name='Carrot',
            category=category2,
            calories=41,
            protein=0.9,
            carbs=10,
            fat=0.2
        )

        response = self.client.get(f"{reverse('calorie:food_list')}?category={category1.id}")
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calorie/food_list.html')
        self.assertContains(response, 'Apple')
        self.assertNotContains(response, 'Carrot')
        self.assertEqual(len(response.context['foods']), 1)

class FoodDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user= User.objects.create_user(
            username='testuser5',
            email='testtuser@gmail.com',
            password='passtest333',
            gender = 'M',
            age= 23,
            height=180,
            weight=80,
        )
        self.category = FoodCategory.objects.create(
            name='Test Category',
        )
        self.food = FoodItem.objects.create(
            name = 'Test Food',
            category=self.category,
            calories=100,
            protein=10,
            carbs=20,
            fat = 5
        )
    def test_food_detail_view_unauthorized(self):
        response = self.client.get(reverse('calorie:food_detail', kwargs={'pk': self.food.pk}))
        self.assertEqual(response.status_code, 302)

    def test_food_detail_view_authorized(self):
        self.client.login(username='testuser5', password='passtest333')
        response = self.client.get(reverse('calorie:food_detail', kwargs={'pk':self.food.pk}))

        self.assertEqual(response.status_code , 200)
        self.assertTemplateUsed(response, 'calorie/food_detail.html')
        self.assertContains(response, 'Test Food')
    
    def test_food_detail_view_404(self):
        self.client.login(username='testuser5', password='passtest333')
        
        food = FoodItem.objects.create(
            name='Food to delete',
            category=self.category,
            calories=100,
            protein=10,
            carbs=20,
            fat=5
        )
        pk_to_test = food.pk
        food.delete()

        response = self.client.get(reverse('calorie:food_detail', kwargs={'pk':pk_to_test}))

        self.assertEqual(response.status_code, 404)
        self.assertContains(response , 'Not Found', status_code=404)

    def test_create_food_log(self):
        self.client.login(username='testuser5', password='passtest333')
        
        from django.utils import timezone
        form_data = {
            'food_item': self.food.pk,
            'amount': 2,
            'meal_type': 'breakfast',
            'date': timezone.now().date()
        }
        response = self.client.post(
            reverse('calorie:food_detail', kwargs={'pk': self.food.pk}),
            data=form_data
        )


        self.assertTrue(UserFoodLog.objects.exists())
        food_log = UserFoodLog.objects.first()
        self.assertEqual(food_log.user, self.user)
        self.assertEqual(food_log.food_item, self.food)
        self.assertEqual(food_log.meal_type, 'breakfast')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('calorie:daily_summary'))

class TestDailySummaryView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user= User.objects.create_user(
            username='testuser5',
            email='testtuser@gmail.com',
            password='passtest333',
            gender = 'M',
            age= 23,
            height=180,
            weight=80,
        )
        self.category = FoodCategory.objects.create(
            name='Test Category',
        )

    def test_daily_summary_view_unauthorized(self):
        response = self.client.get(reverse('calorie:daily_summary'))
        self.assertEqual(response.status_code,302)

    def test_daily_summary_view_current_day(self):
        self.client.login(username='testuser5', password='passtest333')

        food1 = FoodItem.objects.create(
        name='Apple',
        category=self.category,
        calories=50,
        protein=0.5,
        carbs=15,
        fat=0.2
        )
        food2 = FoodItem.objects.create(
            name='Banana',
            category=self.category,
            calories=90,
            protein=1.1,
            carbs=23,
            fat=0.3
        )

        from django.utils import timezone
        today = timezone.now().date()
        
        UserFoodLog.objects.create(
            user=self.user,
            food_item=food1,
            amount=1,
            meal_type='breakfast',
            date=today
        )
        UserFoodLog.objects.create(
            user=self.user,
            food_item=food2,
            amount=2,
            meal_type='lunch',
            date=today
        )
        
        response = self.client.get(reverse('calorie:daily_summary'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calorie/daily_summary.html')
        self.assertContains(response, 'Apple')
        self.assertContains(response, 'Banana')


    def test_daily_summary_view_specific_date(self):
        self.client.login(username='testuser5', password='passtest333')
        
        from django.utils import timezone
        from datetime import timedelta
        
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        food = FoodItem.objects.create(
            name='Apple',
            category=self.category,
            calories=50,
            protein=0.5,
            carbs=15,
            fat=0.2
        )
        
        UserFoodLog.objects.create(
            user=self.user,
            food_item=food,
            amount=1,
            meal_type='breakfast',
            date=yesterday
        )
        
        UserFoodLog.objects.create(
            user=self.user,
            food_item=food,
            amount=1,
            meal_type='breakfast',
            date=today
        )
    
        response = self.client.get(f"{reverse('calorie:daily_summary')}?date={yesterday}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calorie/daily_summary.html')
        
        
        self.assertEqual(UserFoodLog.objects.filter(date=yesterday).count(), 1)

    def test_daily_summary_calculations(self):
        self.client.login(username='testuser5', password='passtest333')
        
        food = FoodItem.objects.create(
            name='Apple',
            category=self.category,
            calories=100,
            protein=1,
            carbs=20,
            fat=0.5
        )
        
        from django.utils import timezone
        today = timezone.now().date()
        
    
        UserFoodLog.objects.create(
            user=self.user,
            food_item=food,
            amount=2,
            meal_type='breakfast',
            date=today
        )
        UserFoodLog.objects.create(
            user=self.user,
            food_item=food,
            amount=1, 
            meal_type='lunch',
            date=today
        )
        
        response = self.client.get(reverse('calorie:daily_summary'))
        self.assertEqual(response.status_code, 200)
        
        
        self.assertContains(response, '300')

    def test_daily_summary_meal_grouping(self):
        self.client.login(username='testuser5', password='passtest333')
        
        food = FoodItem.objects.create(
            name='Apple',
            category=self.category,
            calories=50,
            protein=0.5,
            carbs=15,
            fat=0.2
        )
        
        from django.utils import timezone
        today = timezone.now().date()
        
    
        UserFoodLog.objects.create(
            user=self.user,
            food_item=food,
            amount=1,
            meal_type='breakfast',
            date=today
        )
        UserFoodLog.objects.create(
            user=self.user,
            food_item=food,
            amount=1,
            meal_type='lunch',
            date=today
        )
        UserFoodLog.objects.create(
            user=self.user,
            food_item=food,
            amount=1,
            meal_type='dinner',
            date=today
        )
        
        response = self.client.get(reverse('calorie:daily_summary'))
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, 'Breakfast')
        self.assertContains(response, 'Lunch')
        self.assertContains(response, 'Dinner')

class CustomFoodRequestTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser5',
            email='testuser@gmail.com',
            password='passtest333',
            gender='M',
            age=23,
            height=180,
            weight=80,
        )
        self.category = FoodCategory.objects.create(
            name='Test Category',
        )

    def test_create_food_request(self):
        food_request = CustomFoodRequest.objects.create(
            user=self.user,
            name='New Test Food',
            description='A new healthy food',
            suggested_category=self.category,
            calories=100,
            protein=10,
            carbs=20,
            fat=5
        )
        
        self.assertEqual(food_request.status, 'pending') 
        self.assertEqual(food_request.name, 'New Test Food')
        self.assertEqual(food_request.user, self.user)

class UserFoodLogCalculationsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser5',
            email='testuser@gmail.com',
            password='passtest333',
            gender='M',
            age=23,
            height=180,
            weight=80,
        )
        self.category = FoodCategory.objects.create(
            name='Test Category',
        )
        self.food = FoodItem.objects.create(
            name='Test Food',
            category=self.category,
            calories=100, 
            protein=10,
            carbs=20,
            fat=5
        )
        
    def test_negative_amount_validation(self):
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            log = UserFoodLog.objects.create(
                user=self.user,
                food_item=self.food,
                amount=-1, 
                meal_type='breakfast',
                date=timezone.now().date()
            )
            log.full_clean()

    def test_nutritional_calculations(self):
        log = UserFoodLog.objects.create(
            user=self.user,
            food_item=self.food,
            amount=150,  
            meal_type='breakfast',
            date=timezone.now().date()
        )
        
        
        self.assertEqual(log.calories_consumed, 150)  # 100 * (150/100)
        self.assertEqual(log.protein_consumed, 15)    # 10 * (150/100)
        self.assertEqual(log.carbs_consumed, 30)      # 20 * (150/100)
        self.assertEqual(log.fat_consumed, 7.5)       # 5 * (150/100)

class DailySummarySecurityTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='pass111',
            gender='M',
            age=25,
            height=175,
            weight=75,
        )
    
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='pass222',
            gender='F',
            age=28,
            height=165,
            weight=60,
        )
        
        self.category = FoodCategory.objects.create(name='Test Category')
        self.food = FoodItem.objects.create(
            name='Test Food',
            category=self.category,
            calories=100,
            protein=10,
            carbs=20,
            fat=5
        )

    def test_user_can_only_see_own_logs(self):
        
        today = timezone.now().date()

        UserFoodLog.objects.create(
            user=self.user1,
            food_item=self.food,
            amount=100,
            meal_type='breakfast',
            date=today
        )
        

        UserFoodLog.objects.create(
            user=self.user2,
            food_item=self.food,
            amount=200,
            meal_type='lunch',
            date=today
        )
        

        self.client.login(username='user1', password='pass111')
        response = self.client.get(reverse('calorie:daily_summary'))
        
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context['meals']['breakfast']), 
            1
        ) 
        self.assertEqual(
            len(response.context['meals']['lunch']), 
            0
        ) 