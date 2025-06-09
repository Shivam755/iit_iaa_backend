from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=1000)
    course_code = models.CharField(max_length=10)
    description = models.CharField(max_length=10000)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}({self.course_code})"
    
class CourseInstance(models.Model):
    year = models.CharField(max_length=4, default='')
    semester = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="instances")
