from django.contrib import admin
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


@admin.register(ProgramLearningOutcome)
class ProgramLearningOutcomeAdmin(admin.ModelAdmin):
    list_display = ['number', 'short_name', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['short_name', 'description']
    ordering = ['number']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'semester', 'year', 'grade', 'status']
    list_filter = ['semester', 'year', 'status', 'grade']
    search_fields = ['student__name', 'course__code', 'course__name']
    raw_id_fields = ['student', 'course']


@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = ['course', 'professor', 'semester', 'year', 'section', 'capacity', 'is_active']
    list_filter = ['semester', 'year', 'is_active']
    search_fields = ['course__code', 'course__name', 'professor__name']
    raw_id_fields = ['course', 'professor']


@admin.register(CoursePLOMapping)
class CoursePLOMappingAdmin(admin.ModelAdmin):
    list_display = ['course', 'plo', 'contribution_level', 'weight_percentage']
    list_filter = ['contribution_level']
    search_fields = ['course__code', 'plo__short_name']
    raw_id_fields = ['course', 'plo']


@admin.register(StudentPLOAchievement)
class StudentPLOAchievementAdmin(admin.ModelAdmin):
    list_display = ['student', 'plo', 'enrollment', 'achievement_level', 'score', 'assessed_at']
    list_filter = ['achievement_level', 'assessed_at']
    search_fields = ['student__name', 'plo__short_name']
    raw_id_fields = ['student', 'plo', 'enrollment']
    readonly_fields = ['assessed_at']


@admin.register(LearningOutcome)
class LearningOutcomeAdmin(admin.ModelAdmin):
    list_display = ['code', 'course', 'bloom_level', 'plo', 'weight_percentage', 'is_active']
    list_filter = ['bloom_level', 'is_active', 'course']
    search_fields = ['code', 'description', 'course__code', 'course__name']
    raw_id_fields = ['course', 'plo']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ProgramOutcome)
class ProgramOutcomeAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'outcome_type', 'is_active']
    list_filter = ['outcome_type', 'is_active']
    search_fields = ['code', 'title', 'description']
    filter_horizontal = ['related_plos']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_offering', 'assessment_type', 'max_score', 'weight_percentage', 'due_date', 'is_graded']
    list_filter = ['assessment_type', 'is_graded', 'due_date']
    search_fields = ['name', 'description', 'course_offering__course__code']
    raw_id_fields = ['course_offering']
    filter_horizontal = ['learning_outcomes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'due_date'


@admin.register(AssessmentLOMapping)
class AssessmentLOMappingAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'learning_outcome', 'contribution_percentage']
    search_fields = ['assessment__name', 'learning_outcome__code']
    raw_id_fields = ['assessment', 'learning_outcome']


@admin.register(LOPOMapping)
class LOPOMappingAdmin(admin.ModelAdmin):
    list_display = ['learning_outcome', 'program_outcome', 'weight']
    list_filter = ['weight']
    search_fields = ['learning_outcome__code', 'program_outcome__code']
    raw_id_fields = ['learning_outcome', 'program_outcome']


@admin.register(StudentAssessmentScore)
class StudentAssessmentScoreAdmin(admin.ModelAdmin):
    list_display = ['student', 'assessment', 'score', 'normalized_score_display', 'graded_at']
    list_filter = ['graded_at', 'assessment__assessment_type']
    search_fields = ['student__name', 'assessment__name']
    raw_id_fields = ['student', 'assessment', 'enrollment']
    readonly_fields = ['graded_at', 'normalized_score_display']
    
    def normalized_score_display(self, obj):
        return f"{obj.normalized_score():.2f}%"
    normalized_score_display.short_description = 'Normalized Score'

