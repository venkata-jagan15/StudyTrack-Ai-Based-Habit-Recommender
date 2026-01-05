from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('bulk_analyze/', views.bulk_analyze, name='bulk_analyze'),
    path('register/<str:role>/', views.register_view, name='register'),
    path('login/<str:role>/', views.login_view, name='login'),
    # Fallback/Generic URLs
    path('register/', views.register_view, name='register_generic'),
    path('login/', views.login_view, name='login_generic'),
    path('logout/', views.logout_view, name='logout'),
]
