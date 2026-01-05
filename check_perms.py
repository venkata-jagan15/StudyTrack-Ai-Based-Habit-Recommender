import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_insight.settings')
django.setup()

from django.contrib.auth.models import User

def check_perms(username):
    try:
        user = User.objects.get(username=username)
        print(f"User: {user.username}")
        print(f"is_staff: {user.is_staff}")
        print(f"is_superuser: {user.is_superuser}")
        print(f"is_active: {user.is_active}")
    except User.DoesNotExist:
        print("User not found")

if __name__ == "__main__":
    check_perms('jagan')
