from django.core.management.base import BaseCommand
from outcomes.models import (
    Assessment, AssessmentLOMapping, LOPOMapping,
    StudentAssessmentScore, LearningOutcome, ProgramOutcome,
    Enrollment, CourseOffering
)
from students.models import Student
from courses.models import Course


class Command(BaseCommand):
    help = 'Populate calculation demo data (scores, mappings, percentages)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate calculation demo data...\n')

        # Get existing data
        students = Student.objects.all()
        courses = Course.objects.all()
        assessments = Assessment.objects.all()
        los = LearningOutcome.objects.all()
        pos = ProgramOutcome.objects.all()
        enrollments = Enrollment.objects.filter(status='COMPLETED')

        if not all([students.exists(), assessments.exists(), los.exists(), pos.exists()]):
            self.stdout.write(self.style.ERROR('Missing base data. Run populate_test_data first.'))
            return

        self.stdout.write(f'Found: {students.count()} students, {assessments.count()} assessments, {los.count()} LOs, {pos.count()} POs')

        # Step 1: Create Assessment-LO Mappings (contribution percentages)
        self.stdout.write('\n1. Creating Assessment→LO Mappings (percentages)...')
        alo_mappings_created = 0
        
        # CS201 assessments → CLO-1, CLO-2
        cs201_assessments = Assessment.objects.filter(
            course_offering__course__code='CS201'
        )
        cs201_los = LearningOutcome.objects.filter(course__code='CS201')
        
        if cs201_assessments.exists() and cs201_los.exists():
            clo1 = cs201_los.filter(code='CLO-1').first()
            clo2 = cs201_los.filter(code='CLO-2').first()
            
            for assessment in cs201_assessments:
                if 'Midterm' in assessment.name and clo1:
                    AssessmentLOMapping.objects.get_or_create(
                        assessment=assessment,
                        learning_outcome=clo1,
                        defaults={'contribution_percentage': 30.0}
                    )
                    alo_mappings_created += 1
                elif 'Final' in assessment.name and clo1:
                    AssessmentLOMapping.objects.get_or_create(
                        assessment=assessment,
                        learning_outcome=clo1,
                        defaults={'contribution_percentage': 50.0}
                    )
                    alo_mappings_created += 1
                elif 'Assignment' in assessment.name and clo2:
                    AssessmentLOMapping.objects.get_or_create(
                        assessment=assessment,
                        learning_outcome=clo2,
                        defaults={'contribution_percentage': 20.0}
                    )
                    alo_mappings_created += 1

        # CS301 assessments → CLO-1, CLO-2
        cs301_assessments = Assessment.objects.filter(
            course_offering__course__code='CS301'
        )
        cs301_los = LearningOutcome.objects.filter(course__code='CS301')
        
        if cs301_assessments.exists() and cs301_los.exists():
            clo1 = cs301_los.filter(code='CLO-1').first()
            clo2 = cs301_los.filter(code='CLO-2').first()
            
            for assessment in cs301_assessments:
                if 'Project' in assessment.name and clo1:
                    AssessmentLOMapping.objects.get_or_create(
                        assessment=assessment,
                        learning_outcome=clo1,
                        defaults={'contribution_percentage': 40.0}
                    )
                    alo_mappings_created += 1
                elif 'Quiz' in assessment.name and clo2:
                    AssessmentLOMapping.objects.get_or_create(
                        assessment=assessment,
                        learning_outcome=clo2,
                        defaults={'contribution_percentage': 20.0}
                    )
                    alo_mappings_created += 1

        # CS302 assessments → CLO-1, CLO-2
        cs302_assessments = Assessment.objects.filter(
            course_offering__course__code='CS302'
        )
        cs302_los = LearningOutcome.objects.filter(course__code='CS302')
        
        if cs302_assessments.exists() and cs302_los.exists():
            clo1 = cs302_los.filter(code='CLO-1').first()
            clo2 = cs302_los.filter(code='CLO-2').first()
            
            for assessment in cs302_assessments:
                if 'Project' in assessment.name and clo1:
                    AssessmentLOMapping.objects.get_or_create(
                        assessment=assessment,
                        learning_outcome=clo1,
                        defaults={'contribution_percentage': 60.0}
                    )
                    alo_mappings_created += 1
                elif 'Presentation' in assessment.name and clo2:
                    AssessmentLOMapping.objects.get_or_create(
                        assessment=assessment,
                        learning_outcome=clo2,
                        defaults={'contribution_percentage': 40.0}
                    )
                    alo_mappings_created += 1

        self.stdout.write(f'   Created {alo_mappings_created} Assessment-LO mappings')

        # Step 2: Create LO-PO Mappings (weights 1-5)
        self.stdout.write('\n2. Creating LO→PO Mappings (weights)...')
        lopo_mappings_created = 0
        
        if pos.exists() and los.exists():
            po_a = pos.filter(code='PO-A').first()
            po_b = pos.filter(code='PO-B').first()
            
            if po_a:
                # All CLO-1s contribute to PO-A with weight 5
                for lo in los.filter(code='CLO-1'):
                    LOPOMapping.objects.get_or_create(
                        learning_outcome=lo,
                        program_outcome=po_a,
                        defaults={'weight': 5}
                    )
                    lopo_mappings_created += 1
                
                # All CLO-2s contribute to PO-A with weight 3
                for lo in los.filter(code='CLO-2'):
                    LOPOMapping.objects.get_or_create(
                        learning_outcome=lo,
                        program_outcome=po_a,
                        defaults={'weight': 3}
                    )
                    lopo_mappings_created += 1
            
            if po_b:
                # CLO-3s contribute to PO-B with weight 4
                for lo in los.filter(code='CLO-3'):
                    LOPOMapping.objects.get_or_create(
                        learning_outcome=lo,
                        program_outcome=po_b,
                        defaults={'weight': 4}
                    )
                    lopo_mappings_created += 1

        self.stdout.write(f'   Created {lopo_mappings_created} LO-PO mappings')

        # Step 3: Create Student Assessment Scores (grades)
        self.stdout.write('\n3. Creating Student Assessment Scores (grades)...')
        scores_created = 0
        
        # For each enrollment, create scores for assessments
        for enrollment in enrollments:
            course_assessments = Assessment.objects.filter(
                course_offering__course=enrollment.course
            )
            
            for assessment in course_assessments:
                # Generate realistic scores based on grade
                base_score = self._get_base_score(enrollment.grade)
                import random
                score = min(assessment.max_score, base_score + random.uniform(-5, 5))
                
                StudentAssessmentScore.objects.get_or_create(
                    student=enrollment.student,
                    assessment=assessment,
                    enrollment=enrollment,
                    defaults={
                        'score': round(score, 2),
                        'feedback': f'Good work on {assessment.name}'
                    }
                )
                scores_created += 1

        self.stdout.write(f'   Created {scores_created} student assessment scores')

        # Summary
        self.stdout.write(self.style.SUCCESS(f'\n✅ Calculation demo data populated successfully!'))
        self.stdout.write(f'\nCreated:')
        self.stdout.write(f'  - {alo_mappings_created} Assessment→LO mappings (contribution %)')
        self.stdout.write(f'  - {lopo_mappings_created} LO→PO mappings (weights 1-5)')
        self.stdout.write(f'  - {scores_created} student scores (grades)')
        self.stdout.write(f'\n🎬 Ready for demo! Calculations will work automatically.')
        self.stdout.write(f'\nTest with:')
        self.stdout.write(f'  curl http://127.0.0.1:8000/api/learning-outcomes/')
        self.stdout.write(f'  curl http://127.0.0.1:8000/api/program-outcomes/')
        self.stdout.write(f'  curl http://127.0.0.1:8000/api/enrollments/')

    def _get_base_score(self, grade):
        """Convert letter grade to approximate score"""
        grade_map = {
            'AA': 95,
            'BA': 87,
            'BB': 82,
            'CB': 77,
            'CC': 72,
            'DC': 67,
            'DD': 62,
            'FD': 55,
            'FF': 40,
        }
        return grade_map.get(grade, 75)
