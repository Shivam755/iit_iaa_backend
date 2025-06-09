from rest_framework import serializers
from course.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "course_code", "description", "created_date", "modified_date"]
    