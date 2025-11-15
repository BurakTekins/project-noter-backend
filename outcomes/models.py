from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class ProgramLearningOutcome(models.Model):
    """
    Represents a Program Learning Outcome (PLO) for the engineering program.
    These are the competencies students should achieve upon graduation.
    """
    number = models.IntegerField(unique=True, validators=[MinValueValidator(1)])
    description = models.TextField(
        help_text="Full description of what students should be able to do"
    )
    short_name = models.CharField(
        max_length=100, 
        help_text="Brief identifier (e.g., 'Mathematics & Engineering Knowledge')"
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('KNOWLEDGE', 'Knowledge'),
            ('SKILLS', 'Skills'),
            ('COMPETENCE', 'Competence'),
        ],
        default='KNOWLEDGE'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['number']
        verbose_name = 'Program Learning Outcome'
        verbose_name_plural = 'Program Learning Outcomes'

    def __str__(self):
        return f"PLO-{self.number}: {self.short_name}"


class Enrollment(models.Model):
    """
    Represents a student's enrollment in a specific course.
    Tracks grades and PLO achievements.
    """
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='enrollments')
    semester = models.CharField(
        max_length=20,
        choices=[
            ('FALL', 'Fall'),
            ('SPRING', 'Spring'),
            ('SUMMER', 'Summer'),
        ]
    )
    year = models.IntegerField(validators=[MinValueValidator(2000)])
    grade = models.CharField(
        max_length=2,
        choices=[
            ('AA', 'AA (4.0)'),
            ('BA', 'BA (3.5)'),
            ('BB', 'BB (3.0)'),
            ('CB', 'CB (2.5)'),
            ('CC', 'CC (2.0)'),
            ('DC', 'DC (1.5)'),
            ('DD', 'DD (1.0)'),
            ('FD', 'FD (0.5)'),
            ('FF', 'FF (0.0)'),
        ],
        null=True,
        blank=True
    )
    midterm_grade = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    final_grade = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'Active'),
            ('COMPLETED', 'Completed'),
            ('DROPPED', 'Dropped'),
            ('WITHDRAWN', 'Withdrawn'),
        ],
        default='ACTIVE'
    )
    enrolled_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'course', 'semester', 'year']
        ordering = ['-year', '-semester']
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
        return f"{self.student.name} - {self.course.code} ({self.semester} {self.year})"


class CourseOffering(models.Model):
    """
    Represents a specific offering of a course in a given semester/year.
    Links professors to courses with scheduling info.
    """
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='offerings')
    professor = models.ForeignKey('professors.Professor', on_delete=models.CASCADE, related_name='course_offerings')
    semester = models.CharField(
        max_length=20,
        choices=[
            ('FALL', 'Fall'),
            ('SPRING', 'Spring'),
            ('SUMMER', 'Summer'),
        ]
    )
    year = models.IntegerField(validators=[MinValueValidator(2000)])
    section = models.CharField(max_length=10, default='01')
    capacity = models.IntegerField(default=30, validators=[MinValueValidator(1)])
    schedule = models.CharField(max_length=100, blank=True, help_text="e.g., 'Mon/Wed 10:00-11:30'")
    classroom = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['course', 'semester', 'year', 'section']
        ordering = ['-year', '-semester', 'course']
        verbose_name = 'Course Offering'
        verbose_name_plural = 'Course Offerings'

    def __str__(self):
        return f"{self.course.code} - {self.semester} {self.year} (Section {self.section})"


class CoursePLOMapping(models.Model):
    """
    Maps which PLOs are addressed/assessed in each course.
    Tracks the contribution level of each course to specific PLOs.
    """
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='plo_mappings')
    plo = models.ForeignKey(ProgramLearningOutcome, on_delete=models.CASCADE, related_name='course_mappings')
    contribution_level = models.CharField(
        max_length=20,
        choices=[
            ('INTRODUCTORY', 'Introductory (1)'),
            ('REINFORCING', 'Reinforcing (2)'),
            ('MASTERY', 'Mastery (3)'),
        ],
        default='REINFORCING',
        help_text="Level at which this course addresses the PLO"
    )
    assessment_method = models.TextField(
        blank=True,
        help_text="How this PLO is assessed in the course (e.g., 'Project-based evaluation', 'Written exam')"
    )
    weight_percentage = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Weight of this PLO in overall course assessment"
    )

    class Meta:
        unique_together = ['course', 'plo']
        ordering = ['course', 'plo__number']
        verbose_name = 'Course-PLO Mapping'
        verbose_name_plural = 'Course-PLO Mappings'

    def __str__(self):
        return f"{self.course.code} → PLO-{self.plo.number} ({self.contribution_level})"


class StudentPLOAchievement(models.Model):
    """
    Tracks individual student achievement of specific PLOs through course enrollments.
    This allows monitoring of student progress towards learning outcomes.
    """
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='plo_achievements')
    plo = models.ForeignKey(ProgramLearningOutcome, on_delete=models.CASCADE, related_name='student_achievements')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='plo_achievements')
    achievement_level = models.CharField(
        max_length=20,
        choices=[
            ('NOT_ACHIEVED', 'Not Achieved'),
            ('PARTIALLY', 'Partially Achieved'),
            ('ACHIEVED', 'Achieved'),
            ('EXCEEDED', 'Exceeded'),
        ]
    )
    score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Numerical score for this PLO in this course"
    )
    notes = models.TextField(blank=True)
    assessed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['student', 'plo', 'enrollment']
        ordering = ['-assessed_at']
        verbose_name = 'Student PLO Achievement'
        verbose_name_plural = 'Student PLO Achievements'

    def __str__(self):
        return f"{self.student.name} - PLO-{self.plo.number}: {self.achievement_level}"


class LearningOutcome(models.Model):
    """
    Represents a Course Learning Outcome (CLO) - specific learning objectives for individual courses.
    These are more granular than PLOs and map to specific course content.
    """
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='learning_outcomes')
    code = models.CharField(max_length=20, help_text="e.g., 'CLO-1', 'CLO-2'")
    description = models.TextField(help_text="What students should learn in this course")
    bloom_level = models.CharField(
        max_length=20,
        choices=[
            ('REMEMBER', 'Remember'),
            ('UNDERSTAND', 'Understand'),
            ('APPLY', 'Apply'),
            ('ANALYZE', 'Analyze'),
            ('EVALUATE', 'Evaluate'),
            ('CREATE', 'Create'),
        ],
        help_text="Bloom's Taxonomy cognitive level"
    )
    plo = models.ForeignKey(
        ProgramLearningOutcome, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='learning_outcomes',
        help_text="Which PLO this learning outcome supports"
    )
    weight_percentage = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Weight in course assessment"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['course', 'code']
        unique_together = ['course', 'code']
        verbose_name = 'Learning Outcome'
        verbose_name_plural = 'Learning Outcomes'

    def __str__(self):
        return f"{self.course.code} - {self.code}: {self.description[:50]}"


class ProgramOutcome(models.Model):
    """
    Represents broader program-level outcomes beyond the 11 PLOs.
    Can include institutional goals, accreditation requirements, etc.
    """
    code = models.CharField(max_length=20, unique=True, help_text="e.g., 'PO-A', 'PO-B'")
    title = models.CharField(max_length=200)
    description = models.TextField()
    outcome_type = models.CharField(
        max_length=30,
        choices=[
            ('INSTITUTIONAL', 'Institutional Goal'),
            ('ACCREDITATION', 'Accreditation Requirement'),
            ('DEPARTMENTAL', 'Departmental Objective'),
            ('GRADUATE_ATTRIBUTE', 'Graduate Attribute'),
        ],
        default='INSTITUTIONAL'
    )
    related_plos = models.ManyToManyField(
        ProgramLearningOutcome,
        blank=True,
        related_name='program_outcomes',
        help_text="Which PLOs support this program outcome"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['code']
        verbose_name = 'Program Outcome'
        verbose_name_plural = 'Program Outcomes'

    def __str__(self):
        return f"{self.code}: {self.title}"


class Assessment(models.Model):
    """
    Represents assessment activities used to measure student achievement of learning outcomes.
    Examples: exams, projects, quizzes, assignments, presentations.
    """
    course_offering = models.ForeignKey(
        CourseOffering, 
        on_delete=models.CASCADE, 
        related_name='assessments',
        help_text="Which course offering this assessment belongs to"
    )
    name = models.CharField(max_length=200, help_text="e.g., 'Midterm Exam', 'Final Project'")
    assessment_type = models.CharField(
        max_length=30,
        choices=[
            ('EXAM', 'Exam'),
            ('QUIZ', 'Quiz'),
            ('PROJECT', 'Project'),
            ('ASSIGNMENT', 'Assignment'),
            ('PRESENTATION', 'Presentation'),
            ('LAB', 'Lab Work'),
            ('HOMEWORK', 'Homework'),
            ('PARTICIPATION', 'Class Participation'),
            ('OTHER', 'Other'),
        ]
    )
    description = models.TextField(blank=True)
    max_score = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Maximum possible score"
    )
    weight_percentage = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Weight in final grade"
    )
    due_date = models.DateTimeField(null=True, blank=True)
    learning_outcomes = models.ManyToManyField(
        LearningOutcome,
        blank=True,
        related_name='assessments',
        help_text="Which learning outcomes this assessment measures"
    )
    rubric = models.TextField(
        blank=True,
        help_text="Assessment rubric or grading criteria"
    )
    is_graded = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['course_offering', 'due_date', 'name']
        verbose_name = 'Assessment'
        verbose_name_plural = 'Assessments'

    def __str__(self):
        return f"{self.course_offering.course.code} - {self.name}"
