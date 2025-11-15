from django.db import models
from django.utils import timezone


class Professor(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(
        max_length=50,
        choices=[
            ('PROF', 'Professor'),
            ('ASSOC_PROF', 'Associate Professor'),
            ('ASST_PROF', 'Assistant Professor'),
            ('LECTURER', 'Lecturer'),
            ('INSTRUCTOR', 'Instructor'),
        ],
        default='ASST_PROF'
    )
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    office = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    research_interests = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']
        verbose_name = 'Professor'
        verbose_name_plural = 'Professors'

    def __str__(self):
        return f"{self.get_title_display()} {self.name}"
