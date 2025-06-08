from django.shortcuts import render
from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer

class CoursesViewAll(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
