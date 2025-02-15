from django.urls import path
from .views import WorkoutGoalView, ExperienceLevelView, WorkoutPlanView, UpdateWorkoutPlanView , DownloadWorkoutPlanPDF, ChangePlanSessionView

app_name = 'workoutplan'

urlpatterns = [
    path('goal/',WorkoutGoalView.as_view(), name='goal'),
    path('experience/',ExperienceLevelView.as_view(), name='experience'),
    path('plan/',WorkoutPlanView.as_view(), name='workoutplan'),
    path('update/',UpdateWorkoutPlanView.as_view(), name='update'),
    path('download-pdf/',DownloadWorkoutPlanPDF.as_view(), name='download_pdf'),
    path('change-session/',ChangePlanSessionView.as_view(), name='change_sessions'),
]