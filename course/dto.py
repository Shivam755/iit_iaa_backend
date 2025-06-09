from rest_framework import serializers
from course.models import CourseInstance, Course
from django.db import models

class CourseViewInstanceDTO(serializers.Serializer):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="instances")
    course_title = serializers.CharField(source='course.title')
    course_code = serializers.CharField(source='course.course_code')
    course_id = serializers.CharField(source='course.id')
    year_sem = serializers.SerializerMethodField()
    class Meta:
        model=CourseInstance
        fields = ['id', 'year_sem', 'course_title', 'course_code', 'course_id']
    
    def get_year_sem(self, obj):
        return f"{obj.year}-{obj.semester}"

class CourseCreateInstanceDTO(serializers.Serializer):
    course_id = serializers.CharField(source='course.id')
    year = serializers.IntegerField()
    semester = serializers.IntegerField()

    def validate_course_id(self, value):
        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Course '{value}' does not exist.")
        return value

    def create(self, validated_data):
        print(validated_data)
        course = Course.objects.get(id=validated_data['course']['id'])
        return CourseInstance.objects.create(
            year=validated_data['year'],
            semester=validated_data['semester'],
            course=course
        )

    class Meta:
        model=CourseInstance
        fields = ['course_id', 'year', 'semester']
    