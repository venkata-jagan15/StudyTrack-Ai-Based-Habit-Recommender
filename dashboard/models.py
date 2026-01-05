from django.db import models
from django.contrib.auth.models import User

# User Profile to differentiate roles and store static stats
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    
    # Student specific fields (can be null for teachers)
    grade_level = models.CharField(max_length=10, blank=True, null=True, help_text="e.g. 10th Grade")
    attendance_rate = models.FloatField(default=0.0, help_text="Percentage 0-100")
    predicted_score = models.FloatField(default=0.0, help_text="Current AI predicted score")
    risk_level = models.CharField(max_length=20, default='Safe', help_text="Low, Medium, High")

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Daily habits tracked by the student (Graph: Daily Schedule / Input Form)
class HabitLog(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habit_logs')
    date = models.DateField(auto_now_add=True)
    sleep_hours = models.FloatField()
    study_hours = models.FloatField()
    assignments_completed = models.FloatField(default=0)
    social_media_hours = models.FloatField()
    
    def __str__(self):
        return f"{self.student.username} - {self.date}"

# Subject-wise performance (Graph: Subject Breakdown)
class SubjectGrade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    subject_name = models.CharField(max_length=50) # Math, Science, History, etc.
    score = models.FloatField(help_text="Score out of 100")

    def __str__(self):
        return f"{self.student.username} - {self.subject_name}: {self.score}"

# Weekly test scores for trend analysis (Graph: Performance Trend)
class WeeklyTestScore(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_scores')
    week_number = models.IntegerField(help_text="Week number (1, 2, 3...)")
    avg_score = models.FloatField(help_text="Average score for that week")

    class Meta:
        ordering = ['week_number']

    def __str__(self):
        return f"{self.student.username} - Week {self.week_number}: {self.avg_score}"

# Teacher Feedback messages (Frontend: Teacher Feedback section)
class TeacherFeedback(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_feedback')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedback')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"To {self.student.username}: {self.message[:20]}..."

# AI Generated Recommendations (Frontend: AI Recommendations section)
class AIRecommendation(models.Model):
    cat_choices = [('SLEEP', 'Sleep'), ('FOCUS', 'Focus'), ('SOCIAL', 'Social Media'), ('STUDY', 'Study')]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    category = models.CharField(max_length=20, choices=cat_choices)
    message = models.TextField()
    is_alert = models.BooleanField(default=False, help_text="If true, shows as yellow/red warning")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.category}"
