import os
import django
from django.utils import timezone

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_insight.settings')
django.setup()

from django.contrib.auth.models import User
from dashboard.models import UserProfile, HabitLog, TeacherFeedback, AIRecommendation, SubjectGrade, WeeklyTestScore

def seed():
    print("Seeding database...")

    # 1. Create Student User (Alex)
    alex, created = User.objects.get_or_create(username='alex', email='alex@example.com')
    if created:
        alex.set_password('password123')
        alex.save()
        print("Created user: alex")
    
    # Create User Profile for Alex
    profile, created = UserProfile.objects.get_or_create(user=alex)
    profile.role = 'STUDENT'
    profile.predicted_score = 88.0
    profile.risk_level = 'Low'
    profile.save()

    # 2. Create Teacher User (Mr. Anderson)
    teacher, created = User.objects.get_or_create(username='mr_anderson', email='anderson@example.com')
    if created:
        teacher.set_password('password123')
        teacher.save()
        print("Created user: mr_anderson")

    teacher_profile, created = UserProfile.objects.get_or_create(user=teacher)
    teacher_profile.role = 'TEACHER'
    teacher_profile.save()

    # 3. Add Teacher Feedback
    if not TeacherFeedback.objects.filter(student=alex).exists():
        TeacherFeedback.objects.create(
            teacher=teacher,
            student=alex,
            message="Alex, I noticed your assignment submission rate dropped this week. Let's discuss this during office hours."
        )
        print("Added Teacher Feedback")

    # 4. Add AI Recommendations
    if not AIRecommendation.objects.filter(student=alex).exists():
        AIRecommendation.objects.create(
            student=alex,
            category='SLEEP',
            message="Your average sleep is 5.5 hours. Try to reach 7 hours for better retention.",
            is_alert=False
        )
        AIRecommendation.objects.create(
            student=alex,
            category='SOCIAL',
            message="3+ hours of daily usage is correlating with lower focus scores.",
            is_alert=True
        )
        print("Added AI Recommendations")
    
    print("Database seeded successfully!")

if __name__ == '__main__':
    seed()
