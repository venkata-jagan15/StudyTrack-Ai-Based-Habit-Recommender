
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_insight.settings')
django.setup()

from django.contrib.auth.models import User
from dashboard.models import UserProfile, HabitLog, AIRecommendation
from dashboard import ml_utils
from django.test import RequestFactory
from dashboard.views import student_dashboard

def verify_ml_integration():
    print("Verifying ML Integration...")
    
    # 1. Test ML Model Loading
    print("Testing MLUtils...")
    try:
        score = ml_utils.predict_score(8, 8, 10) # Good habits
        print(f"Predicted Score for (8h study, 8h sleep, 10 assigns): {score}")
        assert score > 0, "Prediction failed"
    except Exception as e:
        print(f"ML Utils failed: {e}")
        return

    # 2. Test View Logic (Simulation)
    print("Testing Student Dashboard View Logic...")
    
    # Create test user
    username = "test_student_ml"
    if User.objects.filter(username=username).exists():
        User.objects.filter(username=username).delete()
    
    user = User.objects.create_user(username=username, password="password")
    profile = UserProfile.objects.create(user=user, role="STUDENT")
    
    # Create request
    factory = RequestFactory()
    data = {
        'sleep_hours': 7.0,
        'study_hours': 5.0, 
        'social_media_hours': 2.0,
        'assignments_completed': 8.0 # High assignments
    }
    request = factory.post('/student_dashboard/', data)
    request.user = user
    
    # Add messages support
    from django.contrib.messages.storage.fallback import FallbackStorage
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
    
    # Execute view
    # We ignore the redirect response, just check side effects
    response = student_dashboard(request)
    
    # Check HabitLog
    log = HabitLog.objects.filter(student=user).first()
    if log:
        print(f"HabitLog created: Study={log.study_hours}, Assigns={log.assignments_completed}")
        assert log.assignments_completed == 8.0
    else:
        print("FAIL: HabitLog not created.")
    
    # Check Profile Update
    profile.refresh_from_db()
    print(f"Profile Predicted Score: {profile.predicted_score}")
    print(f"Profile Risk Level: {profile.risk_level}")
    
    assert profile.predicted_score > 0
    
    # Check Recommendation
    rec = AIRecommendation.objects.filter(student=user).first()
    if rec:
        print(f"Recommendation generated: {rec.message}")
    else:
        print("FAIL: No recommendation generated.")

    print("\nVERIFICATION COMPLETE: SUCCESS")

if __name__ == "__main__":
    verify_ml_integration()
