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


class AssessmentLOMapping(models.Model):
    """
    Maps assessments to learning outcomes with contribution percentage.
    This defines how much each assessment contributes to a specific LO.
    """
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name='lo_mappings'
    )
    learning_outcome = models.ForeignKey(
        LearningOutcome,
        on_delete=models.CASCADE,
        related_name='assessment_mappings'
    )
    contribution_percentage = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="How much this assessment contributes to the LO (0-100%)"
    )

    class Meta:
        unique_together = ['assessment', 'learning_outcome']
        verbose_name = 'Assessment-LO Mapping'
        verbose_name_plural = 'Assessment-LO Mappings'

    def __str__(self):
        return f"{self.assessment.name} → {self.learning_outcome.code} ({self.contribution_percentage}%)"


class LOPOMapping(models.Model):
    """
    Maps learning outcomes to program outcomes with weight (1-5 scale).
    This defines how strongly each LO contributes to a PO.
    """
    learning_outcome = models.ForeignKey(
        LearningOutcome,
        on_delete=models.CASCADE,
        related_name='po_mappings'
    )
    program_outcome = models.ForeignKey(
        ProgramOutcome,
        on_delete=models.CASCADE,
        related_name='lo_mappings'
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Weight of LO contribution to PO (1-5 scale)"
    )

    class Meta:
        unique_together = ['learning_outcome', 'program_outcome']
        verbose_name = 'LO-PO Mapping'
        verbose_name_plural = 'LO-PO Mappings'

    def __str__(self):
        return f"{self.learning_outcome.code} → {self.program_outcome.code} (weight: {self.weight})"


class StudentAssessmentScore(models.Model):
    """
    Stores individual student scores for specific assessments.
    """
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='assessment_scores'
    )
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name='student_scores'
    )
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='assessment_scores'
    )
    score = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Student's score on this assessment"
    )
    feedback = models.TextField(blank=True)
    graded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['student', 'assessment', 'enrollment']
        ordering = ['-graded_at']
        verbose_name = 'Student Assessment Score'
        verbose_name_plural = 'Student Assessment Scores'

    def __str__(self):
        return f"{self.student.name} - {self.assessment.name}: {self.score}/{self.assessment.max_score}"

    def normalized_score(self):
        """Returns score as percentage (0-100)"""
        if self.assessment.max_score > 0:
            return (self.score / self.assessment.max_score) * 100
        return 0.0


# ============================================================================
# CALCULATION FUNCTIONS
# ============================================================================

def calculate_lo_score(learning_outcome, student, enrollment=None):
    """
    Calculate Learning Outcome score for a student.
    
    Formula: LO_Score = Σ(AssessmentGrade * AssessmentWeight)
    
    Args:
        learning_outcome: LearningOutcome instance
        student: Student instance
        enrollment: Optional Enrollment instance (if None, uses latest enrollment for the course)
    
    Returns:
        float: LO score as percentage (0-100)
    """
    from students.models import Student
    from django.db.models import Sum, Q
    
    # Get enrollment if not provided
    if enrollment is None:
        enrollment = Enrollment.objects.filter(
            student=student,
            course=learning_outcome.course,
            status='COMPLETED'
        ).order_by('-year', '-semester').first()
        
        if not enrollment:
            return 0.0
    
    # Get all assessment mappings for this LO
    lo_mappings = AssessmentLOMapping.objects.filter(
        learning_outcome=learning_outcome
    ).select_related('assessment')
    
    if not lo_mappings.exists():
        return 0.0
    
    total_score = 0.0
    total_weight = 0.0
    
    for mapping in lo_mappings:
        # Get student's score for this assessment
        try:
            student_score = StudentAssessmentScore.objects.get(
                student=student,
                assessment=mapping.assessment,
                enrollment=enrollment
            )
            
            # Normalized score (0-100) * contribution percentage (as decimal)
            normalized = student_score.normalized_score()
            weight = mapping.contribution_percentage / 100.0
            
            total_score += normalized * weight
            total_weight += weight
            
        except StudentAssessmentScore.DoesNotExist:
            # If student hasn't taken this assessment, skip it
            continue
    
    # Return weighted average
    if total_weight > 0:
        return total_score / total_weight
    
    return 0.0


def calculate_po_score(program_outcome, student, course=None):
    """
    Calculate Program Outcome score for a student from Learning Outcomes.
    
    Formula: PO_Score = Σ(LO_Score * LO_PO_Weight) / Σ(LO_PO_Weight)
    
    Args:
        program_outcome: ProgramOutcome instance
        student: Student instance
        course: Optional Course instance (if None, calculates across all courses)
    
    Returns:
        float: PO score as percentage (0-100)
    """
    from django.db.models import Q
    
    # Get all LO-PO mappings for this PO
    lo_po_mappings = LOPOMapping.objects.filter(
        program_outcome=program_outcome
    ).select_related('learning_outcome', 'learning_outcome__course')
    
    # Filter by course if specified
    if course:
        lo_po_mappings = lo_po_mappings.filter(learning_outcome__course=course)
    
    if not lo_po_mappings.exists():
        return 0.0
    
    weighted_sum = 0.0
    total_weight = 0.0
    
    for mapping in lo_po_mappings:
        lo = mapping.learning_outcome
        weight = mapping.weight
        
        # Get the most recent enrollment for this course
        enrollment = Enrollment.objects.filter(
            student=student,
            course=lo.course,
            status='COMPLETED'
        ).order_by('-year', '-semester').first()
        
        if enrollment:
            lo_score = calculate_lo_score(lo, student, enrollment)
            
            if lo_score > 0:
                weighted_sum += lo_score * weight
                total_weight += weight
    
    # Return weighted average
    if total_weight > 0:
        return weighted_sum / total_weight
    
    return 0.0


def calculate_all_po_scores(student, use_credits=True):
    """
    Calculate all Program Outcome scores for a student across all courses.
    
    If use_credits=True: PO_Final = Σ(PO_from_course * CourseCredit) / Σ(CourseCredit)
    If use_credits=False: PO_Final = Average of PO scores across courses
    
    Args:
        student: Student instance
        use_credits: Boolean, whether to weight by course credits
    
    Returns:
        dict: {ProgramOutcome: score} mapping
    """
    from courses.models import Course
    
    # Get all active program outcomes
    program_outcomes = ProgramOutcome.objects.filter(is_active=True)
    
    results = {}
    
    for po in program_outcomes:
        # Get all courses that have LOs contributing to this PO
        lo_mappings = LOPOMapping.objects.filter(
            program_outcome=po
        ).select_related('learning_outcome', 'learning_outcome__course')
        
        courses = set(mapping.learning_outcome.course for mapping in lo_mappings)
        
        if not courses:
            results[po] = 0.0
            continue
        
        if use_credits:
            # Credit-weighted calculation
            weighted_sum = 0.0
            total_credits = 0.0
            
            for course in courses:
                # Get completed enrollments for this course
                enrollments = Enrollment.objects.filter(
                    student=student,
                    course=course,
                    status='COMPLETED'
                )
                
                if enrollments.exists():
                    po_score = calculate_po_score(po, student, course)
                    
                    if po_score > 0:
                        weighted_sum += po_score * course.credit
                        total_credits += course.credit
            
            if total_credits > 0:
                results[po] = weighted_sum / total_credits
            else:
                results[po] = 0.0
        else:
            # Simple average across courses
            po_scores = []
            
            for course in courses:
                enrollments = Enrollment.objects.filter(
                    student=student,
                    course=course,
                    status='COMPLETED'
                )
                
                if enrollments.exists():
                    po_score = calculate_po_score(po, student, course)
                    if po_score > 0:
                        po_scores.append(po_score)
            
            if po_scores:
                results[po] = sum(po_scores) / len(po_scores)
            else:
                results[po] = 0.0
    
    return results


def calculate_student_lo_scores(student, course=None):
    """
    Calculate all Learning Outcome scores for a student.
    
    Args:
        student: Student instance
        course: Optional Course instance (if None, calculates for all courses)
    
    Returns:
        dict: {LearningOutcome: score} mapping
    """
    # Get learning outcomes
    learning_outcomes = LearningOutcome.objects.filter(is_active=True)
    
    if course:
        learning_outcomes = learning_outcomes.filter(course=course)
    
    results = {}
    
    for lo in learning_outcomes:
        enrollment = Enrollment.objects.filter(
            student=student,
            course=lo.course,
            status='COMPLETED'
        ).order_by('-year', '-semester').first()
        
        if enrollment:
            results[lo] = calculate_lo_score(lo, student, enrollment)
        else:
            results[lo] = 0.0
    
    return results


def get_student_po_summary(student):
    """
    Get a comprehensive summary of student's Program Outcome achievements.
    
    Args:
        student: Student instance
    
    Returns:
        dict: Comprehensive summary with scores and statistics
    """
    po_scores = calculate_all_po_scores(student, use_credits=True)
    
    summary = {
        'student': student,
        'po_scores': {},
        'statistics': {
            'average_po_score': 0.0,
            'highest_po': None,
            'lowest_po': None,
            'completed_courses': 0,
            'total_credits': 0,
        }
    }
    
    # Format PO scores
    for po, score in po_scores.items():
        summary['po_scores'][po.code] = {
            'title': po.title,
            'score': round(score, 2),
            'achievement_level': _get_achievement_level(score)
        }
    
    # Calculate statistics
    if po_scores:
        scores_only = [s for s in po_scores.values() if s > 0]
        if scores_only:
            summary['statistics']['average_po_score'] = round(sum(scores_only) / len(scores_only), 2)
            
            max_score = max(po_scores.values())
            min_score = min([s for s in po_scores.values() if s > 0], default=0)
            
            for po, score in po_scores.items():
                if score == max_score:
                    summary['statistics']['highest_po'] = po.code
                if score == min_score and score > 0:
                    summary['statistics']['lowest_po'] = po.code
    
    # Get completed courses count
    completed_enrollments = Enrollment.objects.filter(
        student=student,
        status='COMPLETED'
    ).select_related('course')
    
    summary['statistics']['completed_courses'] = completed_enrollments.count()
    summary['statistics']['total_credits'] = sum(
        e.course.credit for e in completed_enrollments
    )
    
    return summary


def _get_achievement_level(score):
    """Helper function to categorize scores into achievement levels"""
    if score >= 85:
        return 'EXCEEDED'
    elif score >= 70:
        return 'ACHIEVED'
    elif score >= 50:
        return 'PARTIALLY'
    else:
        return 'NOT_ACHIEVED'

