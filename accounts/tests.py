from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser, Profile
from .forms import CustomSignupForm

class CustomUserTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@gmail.com',
            'username': 'test@gmail.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'age': 25,
            'gender': 'M',
            'height': 175,
            'weight' : 70
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_create_user(self):
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.first_name , self.user_data['first_name'])
        self.assertEqual(self.user.age, self.user_data['age'])
        self.assertEqual(self.user.height, self.user_data['height'])

    def test_user_str_method(self):
        self.assertEqual(str(self.user), self.user_data['email'])

class SignupViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('account_signup')
        self.signup_data = {
            "email": "test@gmail.com",
            "first_name": "Test",
            "age": 30,
            "gender": "M",
            "height": 180,
            "weight": 75,
            "password1": "Testpass1234@",
            "password2": "Testpass1234@",
        }

    def test_signup_page_status_code(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code , 200)

    def test_signup_form_valid_data(self):
        form = CustomSignupForm(data=self.signup_data)
        self.assertTrue(form.is_valid())

    def test_profile_form_invalid_data(self):
        invalid_data= self.signup_data.copy()
        invalid_data['age'] = 300
        form = CustomSignupForm(data=invalid_data)
        self.assertFalse(form.is_valid())

class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('account_login')
        self.test_user = CustomUser.objects.create_user(
            email="test@gmail.com",
            username="test@gmail.com",
            password="testpass123",
            first_name="Test",
            age=25,
            gender="M",
            height=175,
            weight=70,
        )

    def test_login_page_status_code(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        response = self.client.post(self.login_url,{
            'login': 'test@gmail.com',
            'password': 'testpass123',

        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(self.login_url,{
            'login':'test@gmail.com',
            'password':'TestPass1234',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
