from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, Q
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
from .serializers import (
    ProgramLearningOutcomeSerializer,
    EnrollmentSerializer,
    CourseOfferingSerializer,
    CoursePLOMappingSerializer,
    StudentPLOAchievementSerializer,
    LearningOutcomeSerializer,
    ProgramOutcomeSerializer,
    AssessmentSerializer
)


class ProgramLearningOutcomeViewSet(viewsets.ModelViewSet):
    queryset = ProgramLearningOutcome.objects.all()
    serializer_class = ProgramLearningOutcomeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['short_name', 'description']
    ordering_fields = ['number', 'category']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active PLOs"""
        active_plos = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_plos, many=True)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'course').all()
    serializer_class = EnrollmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__name', 'course__code', 'course__name']
    ordering_fields = ['year', 'semester', 'enrolled_at']
    filterset_fields = ['student', 'course', 'semester', 'year', 'status']

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get enrollments for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'student_id is required'}, status=400)
        
        enrollments = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_course(self, request):
        """Get enrollments for a specific course"""
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response({'error': 'course_id is required'}, status=400)
        
        enrollments = self.queryset.filter(course_id=course_id)
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)


class CourseOfferingViewSet(viewsets.ModelViewSet):
    queryset = CourseOffering.objects.select_related('course', 'professor').all()
    serializer_class = CourseOfferingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['course__code', 'course__name', 'professor__name']
    ordering_fields = ['year', 'semester']
    filterset_fields = ['course', 'professor', 'semester', 'year', 'is_active']

    @action(detail=False, methods=['get'])
    def current_semester(self, request):
        """Get offerings for current semester"""
        semester = request.query_params.get('semester', 'FALL')
        year = request.query_params.get('year', 2025)
        
        offerings = self.queryset.filter(semester=semester, year=year, is_active=True)
        serializer = self.get_serializer(offerings, many=True)
        return Response(serializer.data)


class CoursePLOMappingViewSet(viewsets.ModelViewSet):
    queryset = CoursePLOMapping.objects.select_related('course', 'plo').all()
    serializer_class = CoursePLOMappingSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['course', 'plo__number']
    filterset_fields = ['course', 'plo', 'contribution_level']

    @action(detail=False, methods=['get'])
    def by_course(self, request):
        """Get all PLO mappings for a specific course"""
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response({'error': 'course_id is required'}, status=400)
        
        mappings = self.queryset.filter(course_id=course_id)
        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_plo(self, request):
        """Get all course mappings for a specific PLO"""
        plo_id = request.query_params.get('plo_id')
        if not plo_id:
            return Response({'error': 'plo_id is required'}, status=400)
        
        mappings = self.queryset.filter(plo_id=plo_id)
        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)


class StudentPLOAchievementViewSet(viewsets.ModelViewSet):
    queryset = StudentPLOAchievement.objects.select_related(
        'student', 'plo', 'enrollment__course'
    ).all()
    serializer_class = StudentPLOAchievementSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['assessed_at', 'score']
    filterset_fields = ['student', 'plo', 'enrollment', 'achievement_level']

    @action(detail=False, methods=['get'])
    def student_summary(self, request):
        """Get PLO achievement summary for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'student_id is required'}, status=400)
        
        achievements = self.queryset.filter(student_id=student_id)
        
        # Calculate average score per PLO
        plo_summary = achievements.values('plo__number', 'plo__short_name').annotate(
            avg_score=Avg('score'),
            assessment_count=Count('id')
        ).order_by('plo__number')
        
        return Response({
            'student_id': student_id,
            'plo_achievements': list(plo_summary),
            'total_assessments': achievements.count()
        })

    @action(detail=False, methods=['get'])
    def plo_statistics(self, request):
        """Get overall statistics for a specific PLO across all students"""
        plo_id = request.query_params.get('plo_id')
        if not plo_id:
            return Response({'error': 'plo_id is required'}, status=400)
        
        achievements = self.queryset.filter(plo_id=plo_id)
        
        stats = achievements.aggregate(
            avg_score=Avg('score'),
            total_students=Count('student', distinct=True),
            not_achieved=Count('id', filter=Q(achievement_level='NOT_ACHIEVED')),
            partially=Count('id', filter=Q(achievement_level='PARTIALLY')),
            achieved=Count('id', filter=Q(achievement_level='ACHIEVED')),
            exceeded=Count('id', filter=Q(achievement_level='EXCEEDED'))
        )
        
        return Response(stats)


class LearningOutcomeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course Learning Outcomes (CLOs)
    """
    queryset = LearningOutcome.objects.select_related('course', 'plo').all()
    serializer_class = LearningOutcomeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'description', 'course__code', 'course__name']
    ordering_fields = ['course', 'code', 'bloom_level']
    filterset_fields = ['course', 'plo', 'bloom_level', 'is_active']

    @action(detail=False, methods=['get'])
    def by_course(self, request):
        """Get all learning outcomes for a specific course"""
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response({'error': 'course_id is required'}, status=400)
        
        outcomes = self.queryset.filter(course_id=course_id, is_active=True)
        serializer = self.get_serializer(outcomes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_plo(self, request):
        """Get all learning outcomes supporting a specific PLO"""
        plo_id = request.query_params.get('plo_id')
        if not plo_id:
            return Response({'error': 'plo_id is required'}, status=400)
        
        outcomes = self.queryset.filter(plo_id=plo_id, is_active=True)
        serializer = self.get_serializer(outcomes, many=True)
        return Response(serializer.data)


class ProgramOutcomeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Program Outcomes (broader institutional goals)
    """
    queryset = ProgramOutcome.objects.prefetch_related('related_plos').all()
    serializer_class = ProgramOutcomeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'title', 'description']
    ordering_fields = ['code', 'outcome_type']
    filterset_fields = ['outcome_type', 'is_active']

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get program outcomes by type"""
        outcome_type = request.query_params.get('type')
        if not outcome_type:
            return Response({'error': 'type parameter is required'}, status=400)
        
        outcomes = self.queryset.filter(outcome_type=outcome_type, is_active=True)
        serializer = self.get_serializer(outcomes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def plo_mapping(self, request, pk=None):
        """Get all PLOs related to this program outcome"""
        program_outcome = self.get_object()
        plos = program_outcome.related_plos.all()
        serializer = ProgramLearningOutcomeSerializer(plos, many=True)
        return Response(serializer.data)


class AssessmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for course assessments (exams, projects, assignments, etc.)
    """
    queryset = Assessment.objects.select_related(
        'course_offering__course', 
        'course_offering__professor'
    ).prefetch_related('learning_outcomes').all()
    serializer_class = AssessmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'course_offering__course__code']
    ordering_fields = ['due_date', 'name', 'weight_percentage']
    filterset_fields = ['course_offering', 'assessment_type', 'is_graded']

    @action(detail=False, methods=['get'])
    def by_course_offering(self, request):
        """Get all assessments for a specific course offering"""
        offering_id = request.query_params.get('offering_id')
        if not offering_id:
            return Response({'error': 'offering_id is required'}, status=400)
        
        assessments = self.queryset.filter(course_offering_id=offering_id)
        serializer = self.get_serializer(assessments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming assessments"""
        from django.utils import timezone
        assessments = self.queryset.filter(
            due_date__gte=timezone.now(),
            is_graded=False
        ).order_by('due_date')
        serializer = self.get_serializer(assessments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def learning_outcome_coverage(self, request, pk=None):
        """Get which learning outcomes this assessment covers"""
        assessment = self.get_object()
        learning_outcomes = assessment.learning_outcomes.all()
        serializer = LearningOutcomeSerializer(learning_outcomes, many=True)
        return Response(serializer.data)
