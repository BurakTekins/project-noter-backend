from rest_framework import serializers
from .models import (
    ProgramLearningOutcome, 
    Enrollment, 
    CourseOffering, 
    CoursePLOMapping,
    StudentPLOAchievement,
    LearningOutcome,
    ProgramOutcome,
    Assessment,
    AssessmentLOMapping,
    LOPOMapping,
    StudentAssessmentScore
)


class ProgramLearningOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramLearningOutcome
        fields = ['id', 'number', 'short_name', 'description', 'category', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    lo_scores = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name', 'course', 'course_code', 'course_name',
            'semester', 'year', 'grade', 'midterm_grade', 'final_grade', 
            'status', 'lo_scores', 'enrolled_at', 'completed_at'
        ]
        read_only_fields = ['enrolled_at']
    
    def get_lo_scores(self, obj):
        """
        Automatically calculate all LO scores for this enrollment.
        Only calculates for COMPLETED enrollments.
        """
        if obj.status != 'COMPLETED':
            return None
        
        from .models import LearningOutcome, calculate_lo_score
        
        los = LearningOutcome.objects.filter(course=obj.course, is_active=True)
        scores = []
        
        for lo in los:
            score = calculate_lo_score(lo, obj.student, obj)
            if score > 0:
                scores.append({
                    'lo_code': lo.code,
                    'lo_description': lo.description,
                    'score': round(score, 2),
                    'achievement_level': self._get_achievement_level(score)
                })
        
        return scores if scores else None
    
    def _get_achievement_level(self, score):
        if score >= 85:
            return 'EXCEEDED'
        elif score >= 70:
            return 'ACHIEVED'
        elif score >= 50:
            return 'PARTIALLY'
        else:
            return 'NOT_ACHIEVED'
        read_only_fields = ['enrolled_at']


class CourseOfferingSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    professor_name = serializers.CharField(source='professor.name', read_only=True)
    
    class Meta:
        model = CourseOffering
        fields = [
            'id', 'course', 'course_code', 'course_name', 'professor', 'professor_name',
            'semester', 'year', 'section', 'capacity', 'schedule', 'classroom', 'is_active'
        ]


class CoursePLOMappingSerializer(serializers.ModelSerializer):
    plo_number = serializers.IntegerField(source='plo.number', read_only=True)
    plo_short_name = serializers.CharField(source='plo.short_name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    
    class Meta:
        model = CoursePLOMapping
        fields = [
            'id', 'course', 'course_code', 'plo', 'plo_number', 'plo_short_name',
            'contribution_level', 'assessment_method', 'weight_percentage'
        ]


class StudentPLOAchievementSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    plo_number = serializers.IntegerField(source='plo.number', read_only=True)
    course_code = serializers.CharField(source='enrollment.course.code', read_only=True)
    
    class Meta:
        model = StudentPLOAchievement
        fields = [
            'id', 'student', 'student_name', 'plo', 'plo_number', 
            'enrollment', 'course_code', 'achievement_level', 'score', 
            'notes', 'assessed_at'
        ]
        read_only_fields = ['assessed_at']


class LearningOutcomeSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    plo_number = serializers.IntegerField(source='plo.number', read_only=True, allow_null=True)
    bloom_level_display = serializers.CharField(source='get_bloom_level_display', read_only=True)
    calculated_scores = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = LearningOutcome
        fields = [
            'id', 'course', 'course_code', 'course_name', 'code', 'description',
            'bloom_level', 'bloom_level_display', 'plo', 'plo_number',
            'weight_percentage', 'is_active', 'calculated_scores', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_calculated_scores(self, obj):
        """
        Automatically calculate LO scores for all students who completed this course.
        Returns scores for all students for demo purposes.
        """
        from .models import calculate_lo_score, Enrollment
        
        # Get all completed enrollments for this course
        enrollments = Enrollment.objects.filter(
            course=obj.course,
            status='COMPLETED'
        ).select_related('student')
        
        if not enrollments.exists():
            return []
        
        student_scores = []
        for enrollment in enrollments:
            score = calculate_lo_score(obj, enrollment.student, enrollment)
            if score > 0:
                student_scores.append({
                    'student_id': enrollment.student.id,
                    'student_name': enrollment.student.name,
                    'score': round(score, 2),
                    'achievement_level': self._get_achievement_level(score)
                })
        
        return student_scores if student_scores else []
    
    def _get_achievement_level(self, score):
        if score >= 85:
            return 'EXCEEDED'
        elif score >= 70:
            return 'ACHIEVED'
        elif score >= 50:
            return 'PARTIALLY'
        else:
            return 'NOT_ACHIEVED'


class ProgramOutcomeSerializer(serializers.ModelSerializer):
    outcome_type_display = serializers.CharField(source='get_outcome_type_display', read_only=True)
    related_plo_numbers = serializers.SerializerMethodField()
    calculated_scores = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ProgramOutcome
        fields = [
            'id', 'code', 'title', 'description', 'outcome_type', 'outcome_type_display',
            'related_plos', 'related_plo_numbers', 'calculated_scores', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_related_plo_numbers(self, obj):
        return [plo.number for plo in obj.related_plos.all()]
    
    def get_calculated_scores(self, obj):
        """
        Automatically calculate PO scores for all students.
        Returns scores for all students who have completed relevant courses.
        """
        from .models import calculate_po_score, Enrollment
        from students.models import Student
        
        # Get all students who have completed courses
        completed_enrollments = Enrollment.objects.filter(
            status='COMPLETED'
        ).values_list('student_id', flat=True).distinct()
        
        students = Student.objects.filter(id__in=completed_enrollments)
        
        if not students.exists():
            return []
        
        student_scores = []
        for student in students:
            score = calculate_po_score(obj, student)
            if score > 0:
                student_scores.append({
                    'student_id': student.id,
                    'student_name': student.name,
                    'score': round(score, 2),
                    'achievement_level': self._get_achievement_level(score)
                })
        
        return student_scores if student_scores else []
    
    def _get_achievement_level(self, score):
        if score >= 85:
            return 'EXCEEDED'
        elif score >= 70:
            return 'ACHIEVED'
        elif score >= 50:
            return 'PARTIALLY'
        else:
            return 'NOT_ACHIEVED'


class AssessmentSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course_offering.course.code', read_only=True)
    course_name = serializers.CharField(source='course_offering.course.name', read_only=True)
    semester = serializers.CharField(source='course_offering.semester', read_only=True)
    year = serializers.IntegerField(source='course_offering.year', read_only=True)
    assessment_type_display = serializers.CharField(source='get_assessment_type_display', read_only=True)
    learning_outcome_codes = serializers.SerializerMethodField()
    
    class Meta:
        model = Assessment
        fields = [
            'id', 'course_offering', 'course_code', 'course_name', 'semester', 'year',
            'name', 'assessment_type', 'assessment_type_display', 'description',
            'max_score', 'weight_percentage', 'due_date', 'learning_outcomes',
            'learning_outcome_codes', 'rubric', 'is_graded', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_learning_outcome_codes(self, obj):
        return [lo.code for lo in obj.learning_outcomes.all()]


class AssessmentLOMappingSerializer(serializers.ModelSerializer):
    assessment_name = serializers.CharField(source='assessment.name', read_only=True)
    learning_outcome_code = serializers.CharField(source='learning_outcome.code', read_only=True)
    course_code = serializers.CharField(source='learning_outcome.course.code', read_only=True)
    
    class Meta:
        model = AssessmentLOMapping
        fields = [
            'id', 'assessment', 'assessment_name', 'learning_outcome', 
            'learning_outcome_code', 'course_code', 'contribution_percentage'
        ]


class LOPOMappingSerializer(serializers.ModelSerializer):
    learning_outcome_code = serializers.CharField(source='learning_outcome.code', read_only=True)
    program_outcome_code = serializers.CharField(source='program_outcome.code', read_only=True)
    program_outcome_title = serializers.CharField(source='program_outcome.title', read_only=True)
    
    class Meta:
        model = LOPOMapping
        fields = [
            'id', 'learning_outcome', 'learning_outcome_code', 
            'program_outcome', 'program_outcome_code', 'program_outcome_title', 'weight'
        ]


class StudentAssessmentScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    assessment_name = serializers.CharField(source='assessment.name', read_only=True)
    max_score = serializers.FloatField(source='assessment.max_score', read_only=True)
    normalized_score = serializers.SerializerMethodField()
    course_code = serializers.CharField(source='enrollment.course.code', read_only=True)
    
    class Meta:
        model = StudentAssessmentScore
        fields = [
            'id', 'student', 'student_name', 'assessment', 'assessment_name',
            'enrollment', 'course_code', 'score', 'max_score', 'normalized_score',
            'feedback', 'graded_at'
        ]
        read_only_fields = ['graded_at']
    
    def get_normalized_score(self, obj):
        return round(obj.normalized_score(), 2)

