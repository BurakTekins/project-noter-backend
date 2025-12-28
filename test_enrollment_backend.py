"""
Backend enrollment kontrol scripti
Kurs atama ve enrollment endpoint'lerini test eder
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
from courses.models import Course
from enrollments.models import Enrollment

def test_enrollment_creation():
    """Kurs atama ve enrollment oluşturma testi"""
    print("=" * 60)
    print("BACKEND ENROLLMENT KONTROL TESTİ")
    print("=" * 60)
    print()
    
    # 1. Öğrencileri listele
    students = Student.objects.all()[:5]
    print("📚 Mevcut Öğrenciler:")
    for idx, student in enumerate(students, 1):
        enrollment_count = Enrollment.objects.filter(student=student).count()
        print(f"   {idx}. ID: {student.id} | student_id: '{student.student_id}' | Name: {student.name} | Enrollments: {enrollment_count}")
    print()
    
    # Kullanıcıdan öğrenci seç
    try:
        student_input = input("Test için öğrenci ID'si girin (veya Enter'a basın - ilk öğrenci): ").strip()
        if student_input:
            try:
                student_id = int(student_input)
                student = Student.objects.get(id=student_id)
            except (ValueError, Student.DoesNotExist):
                # String olarak dene (student_id)
                try:
                    student = Student.objects.get(student_id=student_input)
                except Student.DoesNotExist:
                    print(f"❌ Öğrenci bulunamadı: {student_input}")
                    return
        else:
            student = students[0] if students else None
            if not student:
                print("❌ Veritabanında öğrenci yok!")
                return
    except KeyboardInterrupt:
        print("\n❌ İptal edildi")
        return
    
    print(f"\n✅ Seçilen Öğrenci:")
    print(f"   ID: {student.id}")
    print(f"   student_id: '{student.student_id}'")
    print(f"   Name: {student.name}")
    print()
    
    # 2. Mevcut enrollment'ları göster
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    print(f"📋 Mevcut Enrollment'lar ({enrollments.count()} adet):")
    if enrollments.exists():
        for idx, enrollment in enumerate(enrollments, 1):
            print(f"   {idx}. Enrollment ID: {enrollment.id}")
            print(f"      Course: {enrollment.course.code} - {enrollment.course.name}")
            print(f"      Status: {enrollment.status}")
            print(f"      Date: {enrollment.enrollment_date}")
            print()
    else:
        print("   ⚠️  Henüz enrollment yok")
        print()
    
    # 3. Mevcut kursları göster
    courses = Course.objects.all()[:5]
    print("📖 Mevcut Kurslar:")
    for idx, course in enumerate(courses, 1):
        is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()
        status_icon = "✅" if is_enrolled else "❌"
        print(f"   {idx}. ID: {course.id} | Code: {course.code} | Name: {course.name} {status_icon}")
    print()
    
    # 4. Kurs atama simülasyonu
    if courses.exists():
        try:
            course_input = input("Test için kurs ID'si girin (veya Enter'a basın - yeni kurs eklemek için): ").strip()
            if course_input:
                try:
                    course_id = int(course_input)
                    course = Course.objects.get(id=course_id)
                    
                    # Enrollment oluştur (simüle)
                    print(f"\n🔄 Enrollment oluşturuluyor...")
                    enrollment, created = Enrollment.objects.get_or_create(
                        student=student,
                        course=course,
                        defaults={'status': 'active'}
                    )
                    
                    if created:
                        print(f"✅ YENİ enrollment oluşturuldu!")
                        print(f"   Enrollment ID: {enrollment.id}")
                        print(f"   Student: {enrollment.student.name} (ID: {enrollment.student.id})")
                        print(f"   Course: {enrollment.course.code} - {enrollment.course.name}")
                        print(f"   Status: {enrollment.status}")
                    else:
                        print(f"ℹ️  Enrollment zaten mevcut")
                        print(f"   Enrollment ID: {enrollment.id}")
                        print(f"   Status: {enrollment.status}")
                    
                    # 5. Enrollment'ları tekrar kontrol et
                    print(f"\n📋 Güncellenmiş Enrollment'lar:")
                    updated_enrollments = Enrollment.objects.filter(student=student).select_related('course')
                    for idx, enr in enumerate(updated_enrollments, 1):
                        print(f"   {idx}. {enr.course.code} - {enr.course.name} (Status: {enr.status})")
                    
                except (ValueError, Course.DoesNotExist):
                    print(f"❌ Kurs bulunamadı: {course_input}")
        except KeyboardInterrupt:
            print("\n❌ İptal edildi")
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)
    print()
    print("🔍 Endpoint Test URL'leri:")
    print(f"   Enrollments: GET /api/students/{student.id}/enrollments/")
    print(f"   Courses: GET /api/students/{student.id}/courses/")
    print(f"   veya student_id ile:")
    print(f"   Enrollments: GET /api/students/{student.student_id}/enrollments/")
    print(f"   Courses: GET /api/students/{student.student_id}/courses/")

if __name__ == "__main__":
    try:
        test_enrollment_creation()
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}")
        import traceback
        traceback.print_exc()

