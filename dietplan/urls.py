from django.urls import path
from .views import ActivityLevelView, DietGoalView, DietPlanView, UpdateDietPlanView,DownloadDietPlanPDF

app_name = "dietplan"

urlpatterns = [
    path('goal/',DietGoalView.as_view(), name='goal' ),
    path("activity/", ActivityLevelView.as_view(), name='activity'),
    path('plan/',DietPlanView.as_view(), name='plan'),
    path('update/',UpdateDietPlanView.as_view(), name='update_plan' ),
    path('download-pdf/',DownloadDietPlanPDF.as_view(), name='download_pdf'),
]
