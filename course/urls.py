from .views import CourseAPI
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseAPI)

urlpatterns = [
    path('', include(router.urls))
]