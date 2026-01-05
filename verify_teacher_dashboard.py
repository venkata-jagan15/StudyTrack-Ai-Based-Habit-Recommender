
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_insight.settings')
django.setup()

from django.contrib.auth.models import User
from dashboard.models import UserProfile, HabitLog
from django.test import RequestFactory
from dashboard.views import teacher_dashboard

def verify_teacher_dashboard():
    print("Verifying Teacher Dashboard Rendering...")
    
    # Create teacher user
    username = "test_teacher_verify"
    teacher_user, _ = User.objects.get_or_create(username=username)
    if not teacher_user.check_password("password"):
        teacher_user.set_password("password")
        teacher_user.save()
        
    UserProfile.objects.get_or_create(user=teacher_user, defaults={"role": "TEACHER"})
    
    # Create some student data to populate the table (and trigger loop)
    s_user, _ = User.objects.get_or_create(username="test_student_v")
    if not s_user.check_password("password"):
        s_user.set_password("password")
        s_user.save()
        
    UserProfile.objects.update_or_create(user=s_user, defaults={"role": "STUDENT", "predicted_score": 85, "risk_level": "Low"})
    HabitLog.objects.update_or_create(student=s_user, defaults={"study_hours": 5, "sleep_hours": 7, "assignments_completed": 10, "social_media_hours": 1})
    
    # Create request
    factory = RequestFactory()
    request = factory.get('/teacher_dashboard/')
    request.user = teacher_user
    
    try:
        response = teacher_dashboard(request)
        print(f"Response Code: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS: Teacher dashboard rendered successfully.")
            # Basic content check
            content = response.content.decode('utf-8')
            if "test_student_v" in content and "5.0 hrs" in content:
                 print("SUCCESS: Student data found in rendered template.")
            else:
                 print("WARNING: Student data NOT found in rendered template.")

            # Check for new JSON fields
            import json
            if '"sleep": 7.0' in content and '"assignments": 10.0' in content:
                print("SUCCESS: JSON contains sleep/assignments data.")
            else:
                print("FAIL: JSON missing sleep/assignments data.")
        else:
            print("FAIL: Dashboard did not return 200 OK.")
    except Exception as e:
        print(f"FAIL: Exception during rendering: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_teacher_dashboard()
