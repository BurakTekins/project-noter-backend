from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, default='Computer Engineering')
    grade_average = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(4.0)],
        help_text="GPA on 4.0 scale"
    )
    enrollment_year = models.IntegerField(
        validators=[MinValueValidator(2000)],
        help_text="Year student enrolled in program"
    )
    expected_graduation_year = models.IntegerField(
        validators=[MinValueValidator(2000)],
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'Active'),
            ('GRADUATED', 'Graduated'),
            ('SUSPENDED', 'Suspended'),
            ('WITHDRAWN', 'Withdrawn'),
        ],
        default='ACTIVE'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['student_number']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.name} ({self.student_number})"
