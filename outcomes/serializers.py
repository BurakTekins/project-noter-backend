from rest_framework import serializers
from .models import (
    ProgramLearningOutcome, 
    Enrollment, 
    CourseOffering, 
    CoursePLOMapping,
    StudentPLOAchievement,
    LearningOutcome,
    ProgramOutcome,
    Assessment
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
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name', 'course', 'course_code', 'course_name',
            'semester', 'year', 'grade', 'midterm_grade', 'final_grade', 
            'status', 'enrolled_at', 'completed_at'
        ]
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
    
    class Meta:
        model = LearningOutcome
        fields = [
            'id', 'course', 'course_code', 'course_name', 'code', 'description',
            'bloom_level', 'bloom_level_display', 'plo', 'plo_number',
            'weight_percentage', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProgramOutcomeSerializer(serializers.ModelSerializer):
    outcome_type_display = serializers.CharField(source='get_outcome_type_display', read_only=True)
    related_plo_numbers = serializers.SerializerMethodField()
    
    class Meta:
        model = ProgramOutcome
        fields = [
            'id', 'code', 'title', 'description', 'outcome_type', 'outcome_type_display',
            'related_plos', 'related_plo_numbers', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_related_plo_numbers(self, obj):
        return [plo.number for plo in obj.related_plos.all()]


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
