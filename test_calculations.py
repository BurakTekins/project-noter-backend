"""
Test script for calculation logic
Usage: python manage.py shell < test_calculations.py
"""

from students.models import Student
from courses.models import Course
from outcomes.models import (
    LearningOutcome,
    ProgramOutcome,
    Assessment,
    CourseOffering,
    Enrollment,
    AssessmentLOMapping,\
    LOPOMapping,
    StudentAssessmentScore,
    calculate_lo_score,
    calculate_po_score,
    calculate_all_po_scores,
    get_student_po_summary
)
from django.utils import timezone

print("=" * 80)
print("TESTING CALCULATION LOGIC")
print("=" * 80)

# Get or create test data
try:
    student = Student.objects.first()
    if not student:
        print("❌ No students found. Run populate_test_data first.")
        exit(1)
    
    course = Course.objects.first()
    if not course:
        print("❌ No courses found. Run populate_test_data first.")
        exit(1)
    
    print(f"✓ Using student: {student.name}")
    print(f"✓ Using course: {course.code}")
    print()
    
    # Check if we have learning outcomes
    los = LearningOutcome.objects.filter(course=course)
    if not los.exists():
        print("❌ No learning outcomes found for this course.")
        exit(1)
    
    print(f"✓ Found {los.count()} learning outcomes for {course.code}")
    
    # Check if we have program outcomes
    pos = ProgramOutcome.objects.all()
    if not pos.exists():
        print("❌ No program outcomes found. Run populate_test_data first.")
        exit(1)
    
    print(f"✓ Found {pos.count()} program outcomes")
    print()
    
    # Test 1: Calculate LO scores
    print("-" * 80)
    print("TEST 1: Calculate LO Scores")
    print("-" * 80)
    
    for lo in los:
        score = calculate_lo_score(lo, student)
        print(f"{lo.code}: {score:.2f}%")
    
    print()
    
    # Test 2: Calculate PO scores
    print("-" * 80)
    print("TEST 2: Calculate PO Scores (per course)")
    print("-" * 80)
    
    for po in pos:
        score = calculate_po_score(po, student, course)
        print(f"{po.code}: {score:.2f}%")
    
    print()
    
    # Test 3: Calculate all PO scores (credit-weighted)
    print("-" * 80)
    print("TEST 3: Calculate All PO Scores (Credit-Weighted)")
    print("-" * 80)
    
    po_scores = calculate_all_po_scores(student, use_credits=True)
    for po, score in po_scores.items():
        print(f"{po.code} - {po.title}: {score:.2f}%")
    
    print()
    
    # Test 4: Calculate all PO scores (simple average)
    print("-" * 80)
    print("TEST 4: Calculate All PO Scores (Simple Average)")
    print("-" * 80)
    
    po_scores = calculate_all_po_scores(student, use_credits=False)
    for po, score in po_scores.items():
        print(f"{po.code} - {po.title}: {score:.2f}%")
    
    print()
    
    # Test 5: Get comprehensive summary
    print("-" * 80)
    print("TEST 5: Comprehensive PO Summary")
    print("-" * 80)
    
    summary = get_student_po_summary(student)
    print(f"Student: {summary['student'].name}")
    print(f"Average PO Score: {summary['statistics']['average_po_score']}")
    print(f"Highest PO: {summary['statistics']['highest_po']}")
    print(f"Lowest PO: {summary['statistics']['lowest_po']}")
    print(f"Completed Courses: {summary['statistics']['completed_courses']}")
    print(f"Total Credits: {summary['statistics']['total_credits']}")
    print()
    print("PO Scores with Achievement Levels:")
    for po_code, data in summary['po_scores'].items():
        print(f"  {po_code}: {data['score']}% - {data['achievement_level']}")
    
    print()
    print("=" * 80)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
    print("=" * 80)
    
except Exception as e:
    print()
    print("=" * 80)
    print(f"❌ ERROR: {str(e)}")
    print("=" * 80)
    import traceback
    traceback.print_exc()
