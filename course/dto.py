from rest_framework import serializers
from course.models import CourseInstance, Course
from django.db import models

class CourseViewInstanceDTO(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title')
    course_code = serializers.CharField(source='course.course_code')
    course_id = serializers.CharField(source='course.id')
    course_description = serializers.CharField(source='course.description')
    prerequisite_course_names = serializers.SerializerMethodField()
    dependent_course_names = serializers.SerializerMethodField()

    class Meta:
        model=CourseInstance
        fields = ['id', 'year', 'semester', 'course_title', 'course_code', 'course_id', 'prerequisite_course_names', 'dependent_course_names', 'course_description']

    def get_prerequisite_course_names(self, obj):
        return ", ".join([c.title for c in obj.course.prerequisites.all()])

    def get_dependent_course_names(self, obj):
        return ", ".join([c.title for c in obj.course.dependent_courses.all()])
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["course_code"] = data["course_code"].upper() if data["course_code"] else None
        return data



class CourseCreateInstanceDTO(serializers.Serializer):
    course_id = serializers.CharField(source='course.id')
    year = serializers.IntegerField()
    semester = serializers.IntegerField()

    def validate_course_id(self, value):
        if not Course.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Course '{value}' does not exist.")
        return value

    def create(self, validated_data):
        course_id = validated_data['course']['id']
        year = validated_data['year']
        semester = validated_data['semester']
        courseInstance = CourseInstance.objects.filter(year=year, semester=semester, course_id=course_id)
        if courseInstance:
            raise serializers.ValidationError(f"An Instance already exists for course_id:{course_id}, year:{year} and semester:{semester}")
        course = Course.objects.get(id=course_id)
        return CourseInstance.objects.create(
            year=year,
            semester=semester,
            course=course
        )

    class Meta:
        model=CourseInstance
        fields = ['course_id', 'year', 'semester']
    