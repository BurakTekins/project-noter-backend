from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    credit = models.IntegerField()

    def __str__(self):
        return f"{self.code} - {self.name}"
