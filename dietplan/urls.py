from django.urls import path
from .views import ActivityLevelView

app_name = "pages"

urlpatterns = [
    path("", ActivityLevelView.as_view(), name='activity')
]
