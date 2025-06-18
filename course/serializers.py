from rest_framework import serializers
from course.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "course_code", "description", "created_date", "modified_date"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["course_code"] = data["course_code"].upper() if data["course_code"] else None
        return data
    