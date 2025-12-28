"""
Backend endpoint'lerini test etmek için script
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
from admin_api.views import assign_course_to_student, get_student_by_id_or_student_id
from student_api.views import student_courses, student_enrollments, get_student_by_id_or_student_id as get_student
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
import json

def simulate_request(method, path, data=None, student_id=None):
    """API request'i simüle et"""
    factory = APIRequestFactory()
    
    if method == 'GET':
        request = factory.get(path)
    elif method == 'POST':
        request = factory.post(path, data, format='json')
    
    return request

def test_endpoint_summary():
    """Endpoint'leri özet olarak test et"""
    print("=" * 70)
    print("BACKEND ENDPOINT KONTROL RAPORU")
    print("=" * 70)
    print()
    
    # 1. Öğrencileri listele
    students = Student.objects.all()[:3]
    if not students:
        print("❌ Veritabanında öğrenci yok!")
        return
    
    print("📚 TEST İÇİN KULLANILABİLECEK ÖĞRENCİLER:")
    for student in students:
        enrollments_count = Enrollment.objects.filter(student=student).count()
        print(f"   • ID: {student.id} | student_id: '{student.student_id}' | Name: {student.name} | Enrollments: {enrollments_count}")
    print()
    
    # İlk öğrenciyi test için kullan
    test_student = students[0]
    print(f"🧪 TEST ÖĞRENCİSİ: {test_student.name}")
    print(f"   ID: {test_student.id}")
    print(f"   student_id: '{test_student.student_id}'")
    print()
    
    # 2. Helper fonksiyon testi
    print("1️⃣  HELPER FONKSİYON TESTİ (get_student_by_id_or_student_id)")
    print("-" * 70)
    
    # Integer ID ile test
    student_by_id = get_student_by_id_or_student_id(str(test_student.id))
    if student_by_id and student_by_id.id == test_student.id:
        print(f"   ✅ Integer ID testi BAŞARILI: '{test_student.id}' → Öğrenci bulundu")
    else:
        print(f"   ❌ Integer ID testi BAŞARISIZ: '{test_student.id}'")
    
    # String student_id ile test
    student_by_student_id = get_student_by_id_or_student_id(test_student.student_id)
    if student_by_student_id and student_by_student_id.id == test_student.id:
        print(f"   ✅ String student_id testi BAŞARILI: '{test_student.student_id}' → Öğrenci bulundu")
    else:
        print(f"   ❌ String student_id testi BAŞARISIZ: '{test_student.student_id}'")
    print()
    
    # 3. Mevcut enrollment'ları göster
    print("2️⃣  MEVCUT ENROLLMENT'LAR")
    print("-" * 70)
    enrollments = Enrollment.objects.filter(student=test_student).select_related('course')
    if enrollments.exists():
        print(f"   Toplam {enrollments.count()} enrollment bulundu:")
        for idx, enrollment in enumerate(enrollments, 1):
            print(f"   {idx}. Enrollment ID: {enrollment.id}")
            print(f"      Course: {enrollment.course.code} - {enrollment.course.name}")
            print(f"      Status: {enrollment.status}")
    else:
        print("   ⚠️  Henüz enrollment yok")
    print()
    
    # 4. Kursları göster
    courses = Course.objects.all()[:3]
    if courses.exists():
        print("3️⃣  MEVCUT KURSLAR (Test için)")
        print("-" * 70)
        for course in courses:
            is_enrolled = Enrollment.objects.filter(student=test_student, course=course).exists()
            status_icon = "✅ (Zaten kayıtlı)" if is_enrolled else "❌ (Kayıtlı değil)"
            print(f"   • ID: {course.id} | Code: {course.code} | Name: {course.name} {status_icon}")
        print()
    
    # 5. Endpoint URL'lerini göster
    print("4️⃣  ENDPOINT URL'LERİ (Test için)")
    print("-" * 70)
    print(f"   Kurs Atama:")
    print(f"   POST /api/admin/students/{test_student.id}/assign-course/")
    print(f"   POST /api/admin/students/{test_student.student_id}/assign-course/")
    print()
    print(f"   Enrollments:")
    print(f"   GET /api/students/{test_student.id}/enrollments/")
    print(f"   GET /api/students/{test_student.student_id}/enrollments/")
    print()
    print(f"   Courses:")
    print(f"   GET /api/students/{test_student.id}/courses/")
    print(f"   GET /api/students/{test_student.student_id}/courses/")
    print()
    
    # 6. Endpoint fonksiyonlarını test et (mock request ile)
    print("5️⃣  ENDPOINT FONKSİYON TESTİ")
    print("-" * 70)
    
    factory = APIRequestFactory()
    
    # Courses endpoint testi - integer ID
    try:
        request = factory.get(f'/api/students/{test_student.id}/courses/')
        response = student_courses(request, str(test_student.id))
        if response.status_code == 200:
            data = response.data
            if isinstance(data, list):
                print(f"   ✅ Courses endpoint (integer ID) ÇALIŞIYOR")
                print(f"      Status: {response.status_code}")
                print(f"      Response type: Array")
                print(f"      Courses count: {len(data)}")
                if data:
                    print(f"      İlk kurs: {data[0].get('code', 'N/A')} - {data[0].get('name', 'N/A')}")
            else:
                print(f"   ⚠️  Courses endpoint array döndürmüyor: {type(data)}")
        else:
            print(f"   ❌ Courses endpoint hata: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Courses endpoint test hatası: {str(e)}")
    
    # Courses endpoint testi - string student_id
    try:
        request = factory.get(f'/api/students/{test_student.student_id}/courses/')
        response = student_courses(request, test_student.student_id)
        if response.status_code == 200:
            print(f"   ✅ Courses endpoint (string student_id) ÇALIŞIYOR")
            print(f"      Status: {response.status_code}")
            print(f"      Response type: {type(response.data).__name__}")
            print(f"      Courses count: {len(response.data) if isinstance(response.data, list) else 'N/A'}")
        else:
            print(f"   ❌ Courses endpoint (student_id) hata: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Courses endpoint (student_id) test hatası: {str(e)}")
    
    print()
    print("=" * 70)
    print("KONTROL TAMAMLANDI")
    print("=" * 70)
    print()
    print("📝 SONRAKI ADIMLAR:")
    print("   1. Django sunucusunu çalıştırın: python manage.py runserver")
    print("   2. Tarayıcıda endpoint'leri test edin (yukarıdaki URL'ler)")
    print("   3. Frontend'den kurs atama yapın ve response'u kontrol edin")

if __name__ == "__main__":
    try:
        test_endpoint_summary()
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}")
        import traceback
        traceback.print_exc()

