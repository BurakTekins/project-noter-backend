from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from students.models import Student
from courses.models import Course
from professors.models import Professor
from outcomes.models import (
    ProgramLearningOutcome,
    Enrollment,
    CourseOffering,
    CoursePLOMapping,
    StudentPLOAchievement,
    LearningOutcome,
    ProgramOutcome,
    Assessment
)


class Command(BaseCommand):
    help = 'Populates the database with comprehensive test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate test data...'))
        
        # Note: We don't clear existing data to avoid schema issues
        # If you want to clear data, use Django admin or shell
        
        # 1. Create Students
        self.stdout.write('Creating students...')
        students = []
        student_data = [
            {'name': 'Alice Johnson', 'student_number': 'S2021001', 'email': 'alice.johnson@university.edu', 'department': 'Computer Engineering', 'grade_average': 3.75, 'enrollment_year': 2021, 'expected_graduation_year': 2025, 'status': 'ACTIVE'},
            {'name': 'Bob Smith', 'student_number': 'S2021002', 'email': 'bob.smith@university.edu', 'department': 'Computer Engineering', 'grade_average': 3.50, 'enrollment_year': 2021, 'expected_graduation_year': 2025, 'status': 'ACTIVE'},
            {'name': 'Carol White', 'student_number': 'S2022001', 'email': 'carol.white@university.edu', 'department': 'Computer Engineering', 'grade_average': 3.90, 'enrollment_year': 2022, 'expected_graduation_year': 2026, 'status': 'ACTIVE'},
            {'name': 'David Brown', 'student_number': 'S2022002', 'email': 'david.brown@university.edu', 'department': 'Software Engineering', 'grade_average': 3.65, 'enrollment_year': 2022, 'expected_graduation_year': 2026, 'status': 'ACTIVE'},
            {'name': 'Eva Martinez', 'student_number': 'S2023001', 'email': 'eva.martinez@university.edu', 'department': 'Computer Engineering', 'grade_average': 3.85, 'enrollment_year': 2023, 'expected_graduation_year': 2027, 'status': 'ACTIVE'},
        ]
        
        for data in student_data:
            student, created = Student.objects.get_or_create(
                student_number=data['student_number'],
                defaults=data
            )
            students.append(student)
            if created:
                self.stdout.write(f'  Created student: {student.name}')
            else:
                self.stdout.write(f'  Found existing student: {student.name}')
        
        # 2. Create Professors
        self.stdout.write('Creating professors...')
        professors = []
        professor_data = [
            {'name': 'Dr. Sarah Anderson', 'title': 'PROF', 'department': 'Computer Engineering', 'email': 'sarah.anderson@university.edu', 'office': 'ENG-301', 'phone': '+1-555-0101', 'research_interests': 'Artificial Intelligence, Machine Learning'},
            {'name': 'Dr. Michael Chen', 'title': 'ASSOC_PROF', 'department': 'Computer Engineering', 'email': 'michael.chen@university.edu', 'office': 'ENG-302', 'phone': '+1-555-0102', 'research_interests': 'Software Engineering, Algorithms'},
            {'name': 'Dr. Emily Davis', 'title': 'ASST_PROF', 'department': 'Computer Engineering', 'email': 'emily.davis@university.edu', 'office': 'ENG-303', 'phone': '+1-555-0103', 'research_interests': 'Database Systems, Data Science'},
            {'name': 'Dr. Robert Wilson', 'title': 'PROF', 'department': 'Software Engineering', 'email': 'robert.wilson@university.edu', 'office': 'ENG-304', 'phone': '+1-555-0104', 'research_interests': 'Software Architecture, Design Patterns'},
        ]
        
        for data in professor_data:
            professor, created = Professor.objects.get_or_create(
                email=data['email'],
                defaults=data
            )
            professors.append(professor)
            if created:
                self.stdout.write(f'  Created professor: {professor.name}')
            else:
                self.stdout.write(f'  Found existing professor: {professor.name}')
        
        # 3. Create Courses
        self.stdout.write('Creating courses...')
        courses = []
        course_data = [
            {'name': 'Data Structures and Algorithms', 'code': 'CS201', 'credit': 4, 'description': 'Fundamental data structures and algorithms', 'course_level': 'SOPHOMORE', 'is_elective': False},
            {'name': 'Database Systems', 'code': 'CS301', 'credit': 3, 'description': 'Relational databases, SQL, and database design', 'course_level': 'JUNIOR', 'is_elective': False},
            {'name': 'Software Engineering', 'code': 'CS302', 'credit': 4, 'description': 'Software development lifecycle and best practices', 'course_level': 'JUNIOR', 'is_elective': False},
            {'name': 'Artificial Intelligence', 'code': 'CS401', 'credit': 3, 'description': 'Introduction to AI concepts and techniques', 'course_level': 'SENIOR', 'is_elective': True},
            {'name': 'Web Development', 'code': 'CS303', 'credit': 3, 'description': 'Modern web technologies and frameworks', 'course_level': 'JUNIOR', 'is_elective': True},
            {'name': 'Operating Systems', 'code': 'CS304', 'credit': 4, 'description': 'Operating system concepts and implementation', 'course_level': 'JUNIOR', 'is_elective': False},
        ]
        
        for data in course_data:
            course, created = Course.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            courses.append(course)
            if created:
                self.stdout.write(f'  Created course: {course.code} - {course.name}')
            else:
                self.stdout.write(f'  Found existing course: {course.code} - {course.name}')
        
        # Add prerequisites
        courses[1].prerequisites.add(courses[0])  # Database requires Data Structures
        courses[2].prerequisites.add(courses[0])  # Software Engineering requires Data Structures
        courses[3].prerequisites.add(courses[0])  # AI requires Data Structures
        
        # 4. Create Course Offerings
        self.stdout.write('Creating course offerings...')
        offerings = []
        offering_data = [
            {'course': courses[0], 'professor': professors[1], 'semester': 'FALL', 'year': 2024, 'section': '01', 'capacity': 40, 'schedule': 'Mon/Wed 10:00-11:30', 'classroom': 'ENG-201'},
            {'course': courses[1], 'professor': professors[2], 'semester': 'FALL', 'year': 2024, 'section': '01', 'capacity': 35, 'schedule': 'Tue/Thu 13:00-14:30', 'classroom': 'ENG-202'},
            {'course': courses[2], 'professor': professors[3], 'semester': 'FALL', 'year': 2024, 'section': '01', 'capacity': 30, 'schedule': 'Mon/Wed 14:00-16:00', 'classroom': 'ENG-203'},
            {'course': courses[3], 'professor': professors[0], 'semester': 'SPRING', 'year': 2025, 'section': '01', 'capacity': 25, 'schedule': 'Tue/Thu 10:00-11:30', 'classroom': 'ENG-204'},
            {'course': courses[4], 'professor': professors[1], 'semester': 'SPRING', 'year': 2025, 'section': '01', 'capacity': 30, 'schedule': 'Wed/Fri 13:00-14:30', 'classroom': 'LAB-101'},
        ]
        
        for data in offering_data:
            offering, created = CourseOffering.objects.get_or_create(
                course=data['course'],
                semester=data['semester'],
                year=data['year'],
                section=data['section'],
                defaults=data
            )
            offerings.append(offering)
            if created:
                self.stdout.write(f'  Created offering: {offering}')
            else:
                self.stdout.write(f'  Found existing offering: {offering}')
        
        # 5. Get PLOs (should already exist from populate_plos command)
        plos = list(ProgramLearningOutcome.objects.all())
        if not plos:
            self.stdout.write(self.style.WARNING('  No PLOs found. Run "python manage.py populate_plos" first.'))
        else:
            self.stdout.write(f'  Found {len(plos)} PLOs')
        
        # 6. Create Course-PLO Mappings
        if plos:
            self.stdout.write('Creating course-PLO mappings...')
            mapping_data = [
                {'course': courses[0], 'plo': plos[0], 'contribution_level': 'REINFORCING', 'assessment_method': 'Exams and programming assignments', 'weight_percentage': 30},
                {'course': courses[0], 'plo': plos[1], 'contribution_level': 'MASTERY', 'assessment_method': 'Algorithm design projects', 'weight_percentage': 40},
                {'course': courses[1], 'plo': plos[0], 'contribution_level': 'REINFORCING', 'assessment_method': 'Database design project', 'weight_percentage': 25},
                {'course': courses[1], 'plo': plos[3], 'contribution_level': 'MASTERY', 'assessment_method': 'SQL queries and optimization', 'weight_percentage': 35},
                {'course': courses[2], 'plo': plos[2], 'contribution_level': 'MASTERY', 'assessment_method': 'Team software project', 'weight_percentage': 50},
                {'course': courses[2], 'plo': plos[5], 'contribution_level': 'MASTERY', 'assessment_method': 'Group project work', 'weight_percentage': 30},
                {'course': courses[3], 'plo': plos[1], 'contribution_level': 'MASTERY', 'assessment_method': 'AI model development', 'weight_percentage': 40},
                {'course': courses[3], 'plo': plos[4], 'contribution_level': 'REINFORCING', 'assessment_method': 'Research paper and experiments', 'weight_percentage': 30},
            ]
            
            for data in mapping_data:
                mapping, created = CoursePLOMapping.objects.get_or_create(
                    course=data['course'],
                    plo=data['plo'],
                    defaults=data
                )
                if created:
                    self.stdout.write(f'  Created mapping: {mapping}')
                else:
                    self.stdout.write(f'  Found existing mapping: {mapping}')
        
        # 7. Create Enrollments
        self.stdout.write('Creating enrollments...')
        enrollments = []
        enrollment_data = [
            {'student': students[0], 'course': courses[0], 'semester': 'FALL', 'year': 2024, 'grade': 'AA', 'midterm_grade': 88, 'final_grade': 92, 'status': 'COMPLETED'},
            {'student': students[0], 'course': courses[1], 'semester': 'FALL', 'year': 2024, 'grade': 'BA', 'midterm_grade': 82, 'final_grade': 85, 'status': 'COMPLETED'},
            {'student': students[1], 'course': courses[0], 'semester': 'FALL', 'year': 2024, 'grade': 'BB', 'midterm_grade': 75, 'final_grade': 78, 'status': 'COMPLETED'},
            {'student': students[1], 'course': courses[2], 'semester': 'FALL', 'year': 2024, 'grade': 'BA', 'midterm_grade': 80, 'final_grade': 84, 'status': 'COMPLETED'},
            {'student': students[2], 'course': courses[0], 'semester': 'FALL', 'year': 2024, 'grade': 'AA', 'midterm_grade': 90, 'final_grade': 95, 'status': 'COMPLETED'},
            {'student': students[3], 'course': courses[1], 'semester': 'FALL', 'year': 2024, 'status': 'ACTIVE'},
            {'student': students[4], 'course': courses[2], 'semester': 'FALL', 'year': 2024, 'status': 'ACTIVE'},
        ]
        
        for data in enrollment_data:
            enrollment, created = Enrollment.objects.get_or_create(
                student=data['student'],
                course=data['course'],
                semester=data['semester'],
                year=data['year'],
                defaults=data
            )
            enrollments.append(enrollment)
            if created:
                self.stdout.write(f'  Created enrollment: {enrollment}')
            else:
                self.stdout.write(f'  Found existing enrollment: {enrollment}')
        
        # 8. Create Learning Outcomes
        self.stdout.write('Creating learning outcomes...')
        learning_outcomes = []
        lo_data = [
            {'course': courses[0], 'code': 'CLO-1', 'description': 'Understand and implement basic data structures', 'bloom_level': 'APPLY', 'plo': plos[0] if plos else None, 'weight_percentage': 25},
            {'course': courses[0], 'code': 'CLO-2', 'description': 'Analyze algorithm complexity and efficiency', 'bloom_level': 'ANALYZE', 'plo': plos[1] if plos else None, 'weight_percentage': 30},
            {'course': courses[0], 'code': 'CLO-3', 'description': 'Design efficient algorithms for problem solving', 'bloom_level': 'CREATE', 'plo': plos[1] if plos else None, 'weight_percentage': 45},
            {'course': courses[1], 'code': 'CLO-1', 'description': 'Understand relational database concepts', 'bloom_level': 'UNDERSTAND', 'plo': plos[0] if plos else None, 'weight_percentage': 20},
            {'course': courses[1], 'code': 'CLO-2', 'description': 'Design normalized database schemas', 'bloom_level': 'CREATE', 'plo': plos[2] if plos else None, 'weight_percentage': 40},
            {'course': courses[1], 'code': 'CLO-3', 'description': 'Write and optimize SQL queries', 'bloom_level': 'APPLY', 'plo': plos[3] if plos else None, 'weight_percentage': 40},
            {'course': courses[2], 'code': 'CLO-1', 'description': 'Apply software development methodologies', 'bloom_level': 'APPLY', 'plo': plos[2] if plos else None, 'weight_percentage': 30},
            {'course': courses[2], 'code': 'CLO-2', 'description': 'Work effectively in software development teams', 'bloom_level': 'APPLY', 'plo': plos[5] if plos else None, 'weight_percentage': 35},
            {'course': courses[2], 'code': 'CLO-3', 'description': 'Evaluate software quality and testing strategies', 'bloom_level': 'EVALUATE', 'plo': plos[8] if plos else None, 'weight_percentage': 35},
        ]
        
        for data in lo_data:
            lo, created = LearningOutcome.objects.get_or_create(
                course=data['course'],
                code=data['code'],
                defaults=data
            )
            learning_outcomes.append(lo)
            if created:
                self.stdout.write(f'  Created learning outcome: {lo.code} for {lo.course.code}')
            else:
                self.stdout.write(f'  Found existing learning outcome: {lo.code} for {lo.course.code}')
        
        # 9. Create Program Outcomes
        self.stdout.write('Creating program outcomes...')
        po_data = [
            {'code': 'PO-A', 'title': 'Technical Excellence', 'description': 'Demonstrate technical excellence in engineering practice', 'outcome_type': 'INSTITUTIONAL'},
            {'code': 'PO-B', 'title': 'Professional Development', 'description': 'Exhibit professional and ethical behavior', 'outcome_type': 'ACCREDITATION'},
            {'code': 'PO-C', 'title': 'Innovation and Creativity', 'description': 'Show innovation and creative problem solving', 'outcome_type': 'DEPARTMENTAL'},
            {'code': 'PO-D', 'title': 'Global Perspective', 'description': 'Understand global and societal impact of engineering', 'outcome_type': 'GRADUATE_ATTRIBUTE'},
        ]
        
        program_outcomes = []
        for data in po_data:
            po, created = ProgramOutcome.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            program_outcomes.append(po)
            # Link to related PLOs
            if po.code == 'PO-A' and plos:
                po.related_plos.add(plos[0], plos[1], plos[2], plos[3])
            elif po.code == 'PO-B' and plos:
                po.related_plos.add(plos[6], plos[8])
            elif po.code == 'PO-C' and plos:
                po.related_plos.add(plos[2], plos[4], plos[9])
            elif po.code == 'PO-D' and plos:
                po.related_plos.add(plos[7], plos[10])
            if created:
                self.stdout.write(f'  Created program outcome: {po}')
            else:
                self.stdout.write(f'  Found existing program outcome: {po}')
        
        # 10. Create Assessments
        self.stdout.write('Creating assessments...')
        base_date = timezone.now()
        assessment_data = [
            {'course_offering': offerings[0], 'name': 'Midterm Exam', 'assessment_type': 'EXAM', 'description': 'Covers data structures basics', 'max_score': 100, 'weight_percentage': 30, 'due_date': base_date + timedelta(days=45), 'is_graded': True},
            {'course_offering': offerings[0], 'name': 'Final Exam', 'assessment_type': 'EXAM', 'description': 'Comprehensive algorithms exam', 'max_score': 100, 'weight_percentage': 40, 'due_date': base_date + timedelta(days=90), 'is_graded': False},
            {'course_offering': offerings[0], 'name': 'Programming Assignment 1', 'assessment_type': 'ASSIGNMENT', 'description': 'Implement linked list operations', 'max_score': 100, 'weight_percentage': 15, 'due_date': base_date + timedelta(days=21), 'is_graded': True},
            {'course_offering': offerings[1], 'name': 'Database Design Project', 'assessment_type': 'PROJECT', 'description': 'Design and implement a complete database', 'max_score': 100, 'weight_percentage': 40, 'due_date': base_date + timedelta(days=75), 'is_graded': False},
            {'course_offering': offerings[1], 'name': 'SQL Quiz 1', 'assessment_type': 'QUIZ', 'description': 'Basic SQL queries', 'max_score': 50, 'weight_percentage': 10, 'due_date': base_date + timedelta(days=28), 'is_graded': True},
            {'course_offering': offerings[2], 'name': 'Team Project', 'assessment_type': 'PROJECT', 'description': 'Develop software in teams using agile', 'max_score': 100, 'weight_percentage': 50, 'due_date': base_date + timedelta(days=80), 'is_graded': False},
            {'course_offering': offerings[2], 'name': 'Project Presentation', 'assessment_type': 'PRESENTATION', 'description': 'Present final project results', 'max_score': 100, 'weight_percentage': 20, 'due_date': base_date + timedelta(days=85), 'is_graded': False},
        ]
        
        assessments = []
        for data in assessment_data:
            assessment, created = Assessment.objects.get_or_create(
                course_offering=data['course_offering'],
                name=data['name'],
                defaults=data
            )
            assessments.append(assessment)
            # Link assessments to learning outcomes
            course = assessment.course_offering.course
            related_los = learning_outcomes[:3] if course == courses[0] else learning_outcomes[3:6] if course == courses[1] else learning_outcomes[6:9]
            assessment.learning_outcomes.add(*related_los[:2])  # Add first 2 related LOs
            if created:
                self.stdout.write(f'  Created assessment: {assessment.name} for {assessment.course_offering.course.code}')
            else:
                self.stdout.write(f'  Found existing assessment: {assessment.name} for {assessment.course_offering.course.code}')
        
        # 11. Create Student PLO Achievements
        if plos and enrollments:
            self.stdout.write('Creating student PLO achievements...')
            achievement_data = [
                {'student': students[0], 'plo': plos[0], 'enrollment': enrollments[0], 'achievement_level': 'ACHIEVED', 'score': 88, 'notes': 'Strong understanding of algorithms'},
                {'student': students[0], 'plo': plos[1], 'enrollment': enrollments[0], 'achievement_level': 'EXCEEDED', 'score': 92, 'notes': 'Excellent problem-solving skills'},
                {'student': students[0], 'plo': plos[0], 'enrollment': enrollments[1], 'achievement_level': 'ACHIEVED', 'score': 85, 'notes': 'Good database knowledge'},
                {'student': students[1], 'plo': plos[0], 'enrollment': enrollments[2], 'achievement_level': 'ACHIEVED', 'score': 78, 'notes': 'Solid performance'},
                {'student': students[1], 'plo': plos[1], 'enrollment': enrollments[2], 'achievement_level': 'ACHIEVED', 'score': 80, 'notes': 'Good analytical skills'},
                {'student': students[2], 'plo': plos[0], 'enrollment': enrollments[4], 'achievement_level': 'EXCEEDED', 'score': 95, 'notes': 'Outstanding performance'},
            ]
            
            for data in achievement_data:
                achievement, created = StudentPLOAchievement.objects.get_or_create(
                    student=data['student'],
                    plo=data['plo'],
                    enrollment=data['enrollment'],
                    defaults=data
                )
                if created:
                    self.stdout.write(f'  Created achievement: {achievement}')
                else:
                    self.stdout.write(f'  Found existing achievement: {achievement}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Test data population completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created:'))
        self.stdout.write(f'  - {len(students)} students')
        self.stdout.write(f'  - {len(professors)} professors')
        self.stdout.write(f'  - {len(courses)} courses')
        self.stdout.write(f'  - {len(offerings)} course offerings')
        self.stdout.write(f'  - {len(enrollments)} enrollments')
        self.stdout.write(f'  - {len(learning_outcomes)} learning outcomes')
        self.stdout.write(f'  - {len(program_outcomes)} program outcomes')
        self.stdout.write(f'  - {len(assessments)} assessments')
        self.stdout.write(self.style.SUCCESS('\nYou can now test your API endpoints!'))
