from django.urls import path
from .views import ActivityLevelView, DietGoalView, DietPlanView

app_name = "dietplan"

urlpatterns = [
    path('goal/',DietGoalView.as_view(), name='goal' ),
    path("activity/", ActivityLevelView.as_view(), name='activity'),
    path('plan/',DietPlanView.as_view(), name='plan'),
]
