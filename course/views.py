from course.models import Course, CourseInstance
from course.serializers import CourseSerializer
from course.dto import CourseViewInstanceDTO, CourseCreateInstanceDTO
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class CourseAPI(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.dependent_courses.count() > 0:
            return Response({"message": "Course cannot be deleted as it is a dependency for other course(s)"}, status=status.HTTP_409_CONFLICT)
        
        self.perform_destroy(instance)
        return Response({"message": "Course deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class CourseInstanceAPI(APIView):
    def get(self, request, year, semester, courseId = None):
        courseInstance = CourseInstance.objects.filter(year=year, semester=semester)
        if courseId is not None:
            courseInstance = courseInstance.get(course_id=courseId)
            if courseInstance is None:
                return Response({"result": f"No instances found for the year-({year}) and semester-({semester}) and Course Id-({courseId})"}, status=status.HTTP_200_OK)
            return Response(CourseViewInstanceDTO(courseInstance).data, status=status.HTTP_200_OK )
        else:
            if courseInstance is None:
                return Response({"result": f"No instances found for the year-({year}) and semester-({semester})"}, status=status.HTTP_200_OK)
            return Response(CourseViewInstanceDTO(courseInstance, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseCreateInstanceDTO(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if CourseInstance.objects.filter(year=request.data['year'], semester=request.data['semester'], course_id=request.data['course_id']).exists():
            return Response({"error": "An instance with given details already exists"}, status=status.HTTP_400_BAD_REQUEST)
        courseInstance = serializer.save()
        return Response(CourseViewInstanceDTO(courseInstance).data, status=status.HTTP_201_CREATED)

    def delete(self, request, year, semester, courseId):
        courseInstance = CourseInstance.objects.filter(year=year, semester=semester, course_id=courseId)
        if not courseInstance:
            return Response({"error": "No Instance exists with the given details"}, status=status.HTTP_400_BAD_REQUEST)
        courseInstance.delete()
        return Response({"result": "Instance deleted successfully!"}, status=status.HTTP_200_OK)

