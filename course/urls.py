from . import views
from django.urls import path

urlpatterns = [
    path("", views.CoursesViewAll.as_view(), name="view-all-courses")
]