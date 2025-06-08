from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=1000)
    course_code = models.CharField(max_length=10)
    description = models.CharField(max_length=10000)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
