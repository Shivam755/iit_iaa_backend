from .models import Course
from .serializers import CourseSerializer
from rest_framework.viewsets import ModelViewSet


class CourseAPI(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



