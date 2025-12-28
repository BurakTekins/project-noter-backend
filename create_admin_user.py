"""
Django admin superuser oluşturma scripti
Kullanım: python create_admin_user.py
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

def create_superuser():
    username = input("Username (örnek: admin): ").strip() or "admin"
    email = input("Email (opsiyonel, Enter'a basarak geçebilirsiniz): ").strip() or ""
    password = input("Password: ").strip()
    
    if not password:
        print("❌ Password gerekli!")
        return
    
    # Kullanıcı zaten var mı kontrol et
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"✅ Mevcut kullanıcı '{username}' superuser yapıldı!")
    else:
        # Yeni kullanıcı oluştur
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Yeni superuser '{username}' oluşturuldu!")
    
    print(f"\n🎉 Artık admin panele giriş yapabilirsiniz:")
    print(f"   URL: http://localhost:8000/admin/")
    print(f"   Username: {username}")
    print(f"   Password: {password}")

if __name__ == "__main__":
    print("=" * 60)
    print("Django Admin Superuser Oluşturma")
    print("=" * 60)
    create_superuser()

