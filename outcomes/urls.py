from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProgramLearningOutcomeViewSet,
    EnrollmentViewSet,
    CourseOfferingViewSet,
    CoursePLOMappingViewSet,
    StudentPLOAchievementViewSet,
    LearningOutcomeViewSet,
    ProgramOutcomeViewSet,
    AssessmentViewSet,
    AssessmentLOMappingViewSet,
    LOPOMappingViewSet,
    StudentAssessmentScoreViewSet
)

router = DefaultRouter()
router.register(r'plos', ProgramLearningOutcomeViewSet, basename='plo')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'offerings', CourseOfferingViewSet, basename='offering')
router.register(r'course-plo-mappings', CoursePLOMappingViewSet, basename='course-plo-mapping')
router.register(r'achievements', StudentPLOAchievementViewSet, basename='achievement')
router.register(r'learning-outcomes', LearningOutcomeViewSet, basename='learning-outcome')
router.register(r'program-outcomes', ProgramOutcomeViewSet, basename='program-outcome')
router.register(r'assessments', AssessmentViewSet, basename='assessment')
router.register(r'assessment-lo-mappings', AssessmentLOMappingViewSet, basename='assessment-lo-mapping')
router.register(r'lo-po-mappings', LOPOMappingViewSet, basename='lo-po-mapping')
router.register(r'student-scores', StudentAssessmentScoreViewSet, basename='student-score')

urlpatterns = [
    path('', include(router.urls)),
]
