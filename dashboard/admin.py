from django.contrib import admin
from .models import UserProfile, HabitLog, SubjectGrade, WeeklyTestScore, TeacherFeedback, AIRecommendation

admin.site.register(UserProfile)
admin.site.register(HabitLog)
admin.site.register(SubjectGrade)
admin.site.register(WeeklyTestScore)
admin.site.register(TeacherFeedback)
admin.site.register(AIRecommendation)
