from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import MuscleViewSet, ExerciseViewSet

router = DefaultRouter()
router.register('muscles', MuscleViewSet, basename='muscle')
router.register('exercises', ExerciseViewSet, basename='exercise')

urlpatterns = [
    path('', include(router.urls)),
]