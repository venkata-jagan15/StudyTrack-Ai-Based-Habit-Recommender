import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_insight.settings')
django.setup()

from django.contrib.auth.models import User
from dashboard.models import UserProfile

def check_user_data(username):
    try:
        user = User.objects.get(username=username)
        print(f"User '{username}' found. ID: {user.id}")
        
        try:
            profile = user.userprofile
            print(f"Profile found. Role: {profile.role}")
        except UserProfile.DoesNotExist:
            print("CRITICAL: User has NO profile.")
            # Create one to fix the error
            UserProfile.objects.create(user=user, role='STUDENT')
            print("Created missing profile (Default: STUDENT).")
            
    except User.DoesNotExist:
        print(f"User '{username}' does not exist.")

if __name__ == "__main__":
    check_user_data('jagan')
