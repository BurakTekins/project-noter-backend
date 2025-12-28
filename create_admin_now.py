"""
Hızlı superuser oluşturma - otomatik
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

from django.contrib.auth.models import User

# Admin kullanıcı bilgileri
USERNAME = 'admin'
EMAIL = 'admin@example.com'
PASSWORD = 'admin123'  # Geliştirme için basit şifre

print("=" * 60)
print("Django Admin Superuser Oluşturuluyor...")
print("=" * 60)

# Kullanıcı zaten var mı kontrol et
if User.objects.filter(username=USERNAME).exists():
    user = User.objects.get(username=USERNAME)
    user.set_password(PASSWORD)
    user.is_superuser = True
    user.is_staff = True
    user.email = EMAIL
    user.save()
    print(f"✅ Mevcut kullanıcı '{USERNAME}' güncellendi!")
else:
    # Yeni superuser oluştur
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print(f"✅ Yeni superuser '{USERNAME}' oluşturuldu!")

print("\n" + "=" * 60)
print("🎉 BAŞARILI!")
print("=" * 60)
print(f"\nAdmin panele giriş bilgileri:")
print(f"   URL:      http://localhost:8000/admin/")
print(f"   Username: {USERNAME}")
print(f"   Password: {PASSWORD}")
print("\n" + "=" * 60)

