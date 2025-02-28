from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MuscleViewSet, ExerciseViewSet, MuscleListView, MuscleDetailView

app_name = 'exercises'

router = DefaultRouter()
router.register('muscles', MuscleViewSet, basename='api_muscle')
router.register('exercises', ExerciseViewSet, basename='api_exercise')

urlpatterns = [
    path('muscles/', MuscleListView.as_view(), name='muscles_list'),
    path('muscles/<int:pk>/', MuscleDetailView.as_view(), name='muscle_detail'),
    # API endpoints
    path('api/', include(router.urls)),
]