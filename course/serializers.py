from rest_framework import serializers
from course.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "course_code", "description", "prerequisites", "dependent_courses", "created_date", "modified_date"]

    def validate_course_code(self, value):
        if Course.objects.filter(course_code=value.lower()).exists():
            raise serializers.ValidationError(f"Course code '{value}' already exists.")
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["course_code"] = data["course_code"].upper() if data["course_code"] else None
        return data
    