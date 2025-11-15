from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    credit = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    description = models.TextField(blank=True)
    course_level = models.CharField(
        max_length=20,
        choices=[
            ('FRESHMAN', 'Freshman (100-level)'),
            ('SOPHOMORE', 'Sophomore (200-level)'),
            ('JUNIOR', 'Junior (300-level)'),
            ('SENIOR', 'Senior (400-level)'),
            ('GRADUATE', 'Graduate (500+ level)'),
        ],
        default='FRESHMAN'
    )
    prerequisites = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='prerequisite_for'
    )
    is_elective = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['code']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f"{self.code} - {self.name}"
