from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_number = models.CharField(max_length=20, unique=True)
    grade_average = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
