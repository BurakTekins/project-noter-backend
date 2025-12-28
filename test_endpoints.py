"""
Backend endpoint'lerini test etmek için script
Kullanım: python test_endpoints.py
"""

import os
import sys
import django

# Django setup
base_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(base_dir, 'project-noter-backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from students.models import Student
from enrollments.models import Enrollment
from courses.models import Course

def test_enrollments(student_id):
    """Enrollment kayıtlarını test et"""
    try:
        student = Student.objects.get(id=student_id)
        enrollments = Enrollment.objects.filter(student=student).select_related('course')
        
        print(f"\n=== Enrollment Test (Student ID: {student_id}) ===")
        print(f"Student: {student.name} ({student.student_id})")
        print(f"Total Enrollments: {enrollments.count()}\n")
        
        if enrollments.exists():
            for idx, enrollment in enumerate(enrollments, 1):
                print(f"{idx}. Enrollment ID: {enrollment.id}")
                print(f"   Course: {enrollment.course.code} - {enrollment.course.name}")
                print(f"   Status: {enrollment.status}")
                print(f"   Date: {enrollment.enrollment_date}")
                print()
        else:
            print("⚠️  No enrollments found!")
            
        return enrollments
    except Student.DoesNotExist:
        print(f"❌ Student with ID {student_id} not found!")
        return None

def test_courses(student_id):
    """Courses endpoint'ini simüle et"""
    try:
        student = Student.objects.get(id=student_id)
        enrollments = Enrollment.objects.filter(
            student=student
        ).select_related('course', 'course__professor').order_by('-enrollment_date')
        
        print(f"\n=== Courses Endpoint Test (Student ID: {student_id}) ===")
        courses = [enrollment.course for enrollment in enrollments if enrollment.course]
        
        if courses:
            print(f"Total Courses: {len(courses)}\n")
            for idx, course in enumerate(courses, 1):
                print(f"{idx}. Course ID: {course.id}")
                print(f"   Code: {course.code}")
                print(f"   Name: {course.name}")
                print(f"   Professor: {course.professor.name if course.professor else 'None'}")
                print()
        else:
            print("⚠️  No courses found! (Empty array [])")
            
        return courses
    except Student.DoesNotExist:
        print(f"❌ Student with ID {student_id} not found!")
        return None

def test_learning_outcomes(student_id):
    """Learning Outcomes endpoint'ini simüle et"""
    try:
        student = Student.objects.get(id=student_id)
        from learning_outcomes.models import LearningOutcome
        
        enrollments = Enrollment.objects.filter(student=student).select_related('course')
        courses = [e.course for e in enrollments if e.course]
        active_enrollments = Enrollment.objects.filter(student=student, status='active')
        course_ids = [e.course.id for e in active_enrollments if e.course]
        
        los = LearningOutcome.objects.filter(course_id__in=course_ids).distinct()
        
        print(f"\n=== Learning Outcomes Endpoint Test (Student ID: {student_id}) ===")
        print(f"Courses array length: {len(courses)}")
        print(f"Learning Outcomes array length: {los.count()}\n")
        
        print("Response format:")
        print("{")
        print(f'  "courses": [array with {len(courses)} courses],')
        print(f'  "learning_outcomes": [array with {los.count()} learning outcomes]')
        print("}")
        
        return {'courses': courses, 'learning_outcomes': list(los)}
    except Student.DoesNotExist:
        print(f"❌ Student with ID {student_id} not found!")
        return None

def list_all_students():
    """Tüm öğrencileri listele"""
    students = Student.objects.all()[:10]  # İlk 10 öğrenci
    print("\n=== Available Students ===")
    for student in students:
        enrollment_count = Enrollment.objects.filter(student=student).count()
        print(f"ID: {student.id} | Name: {student.name} | Enrollments: {enrollment_count}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("BACKEND ENDPOINT TEST SCRIPT")
    print("=" * 60)
    
    # Tüm öğrencileri listele
    list_all_students()
    
    # Kullanıcıdan student ID al
    try:
        student_id = int(input("Enter Student ID to test (or press Enter to test first student): ").strip() or "1")
    except ValueError:
        student_id = 1
    
    # Testleri çalıştır
    enrollments = test_enrollments(student_id)
    courses = test_courses(student_id)
    learning_outcomes_data = test_learning_outcomes(student_id)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

