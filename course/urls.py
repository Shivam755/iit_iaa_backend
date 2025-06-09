from course.views import CourseAPI, CourseInstanceAPI
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseAPI)

urlpatterns = [
    path('instances/', CourseInstanceAPI.as_view(), name='create-delete-instance'),
    path('instances/<int:year>/<int:semester>/', CourseInstanceAPI.as_view(), name='view-instances-for-year-sem'),
    path('instances/<int:year>/<int:semester>/<int:courseId>/', CourseInstanceAPI.as_view(), name='view-instances-for-year-sem-courseId'),
    path('', include(router.urls))
]