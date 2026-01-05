from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, TeacherFeedback, AIRecommendation, HabitLog
from .forms import UserRegisterForm, UserLoginForm
import json
import pandas as pd
from . import ml_utils

def index(request):
    return render(request, 'dashboard/index.html')

def register_view(request, role=None):
    if role:
        role = role.upper() # Ensure STUDENT/TEACHER

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            # Use the role from URL if present and valid, otherwise from form
            selected_role = form.cleaned_data.get('role')
            if role in ['STUDENT', 'TEACHER']:
                final_role = role
            else:
                final_role = selected_role
            
            UserProfile.objects.create(user=user, role=final_role)
            
            login(request, user)
            if final_role == 'STUDENT':
                return redirect('student_dashboard')
            else:
                return redirect('teacher_dashboard')
    else:
        # Pre-select role if provided
        initial_data = {}
        if role:
            initial_data['role'] = role
        form = UserRegisterForm(initial=initial_data)
    
    return render(request, 'dashboard/register.html', {'form': form, 'url_role': role})

def login_view(request, role=None):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                # Optional: Check if the user's role matches the requested login page?
                # For now, let's just log them in regardless, but redirect correctly.
                login(request, user)
                try:
                    user_role = user.userprofile.role
                    if user_role == 'STUDENT':
                        return redirect('student_dashboard')
                    else:
                        return redirect('teacher_dashboard')
                except UserProfile.DoesNotExist:
                     return redirect('student_dashboard')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UserLoginForm()
    return render(request, 'dashboard/login.html', {'form': form, 'url_role': role})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def student_dashboard(request):
    student_user = request.user
    
    try:
        profile = student_user.userprofile
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        try:
            sleep = float(request.POST.get('sleep_hours', 0))
            study = float(request.POST.get('study_hours', 0))
            social = float(request.POST.get('social_media_hours', 0))
            assignments = float(request.POST.get('assignments_completed', 0))
            
            # 1. Save Habit Log
            HabitLog.objects.create(
                student=student_user,
                sleep_hours=sleep,
                study_hours=study,
                social_media_hours=social,
                assignments_completed=assignments
            )
            
            # 2. ML Prediction
            predicted = ml_utils.predict_score(study, sleep, assignments)
            
            # 3. Update Profile
            if profile:
                profile.predicted_score = round(predicted, 2)
                # Simple risk logic based on score
                if predicted < 50:
                    profile.risk_level = 'High'
                elif predicted < 75:
                    profile.risk_level = 'Medium'
                else:
                    profile.risk_level = 'Low'
                profile.save()
            
            # 4. Generate Recommendation
            rec_text = ml_utils.get_recommendation(study, sleep, assignments, predicted)
            
            # Map simplified text to category (naive mapping)
            cat = 'STUDY'
            if 'sleep' in rec_text.lower(): cat = 'SLEEP'
            elif 'social' in rec_text.lower(): cat = 'SOCIAL'
            
            AIRecommendation.objects.create(
                student=student_user,
                category=cat,
                message=rec_text,
                is_alert=(profile.risk_level == 'High')
            )
            
            messages.success(request, "Habits updated! AI has recalculated your score.")
            return redirect('student_dashboard')
            
        except ValueError:
            messages.error(request, "Invalid input. Please enter numbers.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    feedback = TeacherFeedback.objects.filter(student=student_user).order_by('-created_at').first()
    recommendations = AIRecommendation.objects.filter(student=student_user).order_by('-created_at')[:5]
    latest_log = HabitLog.objects.filter(student=student_user).order_by('-date').first()

    context = {
        'student': student_user,
        'profile': profile,
        'feedback': feedback,
        'recommendations': recommendations,
        'latest_log': latest_log
    }
    return render(request, 'dashboard/student_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    teacher_user = request.user
    
    # Fetch all students
    students = UserProfile.objects.filter(role='STUDENT').select_related('user')
    
    # Fetch recent feedback sent by this teacher
    recent_feedback = TeacherFeedback.objects.filter(teacher=teacher_user).order_by('-created_at')[:5]
    
    # Prepare data for charts
    student_data = []
    for s in students:
        # Get latest habit log for study hours
        last_log = HabitLog.objects.filter(student=s.user).order_by('-date').first()
        study_h = last_log.study_hours if last_log else 0
        sleep_h = last_log.sleep_hours if last_log else 0
        assigns = last_log.assignments_completed if last_log else 0
        
        # Calculate cluster on the fly (or store it in profile if performance matters)
        cluster = ml_utils.predict_cluster(study_h, sleep_h, assigns, s.predicted_score)
        
        student_data.append({
            'id': s.user.id,
            'name': s.user.username,
            'study': study_h,
            'sleep': sleep_h,
            'assignments': assigns,
            'social': last_log.social_media_hours if last_log else 0,
            'score': s.predicted_score,
            'risk': s.risk_level,
            'cluster': cluster
        })
        
    context = {
        'teacher': teacher_user,
        'students': students,
        'recent_feedback': recent_feedback,
        'student_data_json': student_data,
        'student_data_list': student_data
    }
    return render(request, 'dashboard/teacher_dashboard.html', context)

def bulk_analyze(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        try:
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a valid CSV file.")
                return redirect('teacher_dashboard')

            df = pd.read_csv(csv_file)
            
            # Column mapping (CSV header -> internal name)
            col_map = {
                'Study_Hours_Per_Day': 'Study_Hours',
                'Study_Hours': 'Study_Hours',
                'Sleep_Hours': 'Sleep_Hours',
                'Assignments_Completed': 'Assignments_Completed',
                'Social_Media_Hours': 'Social_Media_Hours'
            }
            
            # Normalize columns
            df.rename(columns=col_map, inplace=True)

            # Expected columns
            required_cols = ['Study_Hours', 'Sleep_Hours', 'Assignments_Completed', 'Social_Media_Hours']
            
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                 messages.error(request, f"CSV is missing columns: {', '.join(missing_cols)}")
                 return redirect('teacher_dashboard')

            results = []
            for _, row in df.iterrows():
                study = row['Study_Hours']
                sleep = row['Sleep_Hours']
                assigns = row['Assignments_Completed']
                social = row['Social_Media_Hours']
                
                score = ml_utils.predict_score(study, sleep, assigns)
                cluster = ml_utils.predict_cluster(study, sleep, assigns, score)
                
                risk = 'Low'
                if score < 50: risk = 'High'
                elif score < 75: risk = 'Medium'
                
                cluster_label = "Balanced"
                if cluster == 0: cluster_label = "Needs Improvement"
                elif cluster == 2: cluster_label = "Sleep Focus"

                results.append({
                    'study': study,
                    'sleep': sleep,
                    'assigns': assigns,
                    'social': social,
                    'score': round(score, 2),
                    'risk': risk,
                    'cluster': cluster_label
                })
            
            # We need to re-render the dashboard with these results
            # To do this cleanly without duplicating the dashboard logic, 
            # we can store results in session or just call teacher_dashboard with extra context.
            # For simplicity, let's just pass it to the render context of teacher_dashboard
            
            # Since we can't easily "call" the other view and merge context without a redirect loop or code duplication,
            # let's refactor slightly. Actually, easiest is to redirect with ID, but data is too big.
            # Let's render 'teacher_dashboard.html' directly here, but we need the OTHER dashboard data too.
            # A better approach: The dashboard view itself handles the POST if it's on the same URL, 
            # OR we make this a separate page. The user asked for "option to analyze", usually implies same dash.
            # Let's try to just render a "results only" page or re-fetch dashboard data.
            # Valid Re-fetch:
            
            # Fetch Teacher Dashboard Data (Duplicated for now, or extract to helper)
            teacher_user = request.user 
            students = UserProfile.objects.filter(role='STUDENT')
            student_data = []
            for s in students:
                last_log = HabitLog.objects.filter(student=s.user).order_by('-date').first()
                # ... (logic from teacher_dashboard) ...
                # To avoid massive duplication, let's just render a simpler "Analysis Results" template 
                # or just the dashboard with ONLY the results if the user accepts that. 
                # BUT the user likely wants to see it IN the dashboard.
                
                # Compromise: Extract student_data logic to helper if strict, 
                # but for this snippet I will copy the minimal needed context or just return the results 
                # and let the frontend show a "Back to Dashboard" button.
                # Actually, let's just render a new simple template 'dashboard/bulk_results.html' 
                # OR pass it back to teacher_dashboard.html if we fetch the base data.
                
                # Let's fetch base data again (it's not much code)
                pass
            
            # RE-FETCH basic data to keep dashboard valid
            students_all = UserProfile.objects.filter(role='STUDENT')
            student_data_dash = []
            for s in students_all:
                last_log = HabitLog.objects.filter(student=s.user).order_by('-date').first()
                val_study = last_log.study_hours if last_log else 0
                val_sleep = last_log.sleep_hours if last_log else 0
                val_assign = last_log.assignments_completed if last_log else 0
                val_social = last_log.social_media_hours if last_log else 0
                
                cluster_val = ml_utils.predict_cluster(val_study, val_sleep, val_assign, s.predicted_score)

                student_data_dash.append({
                    'id': s.user.id, 'name': s.user.username,
                    'study': val_study, 'sleep': val_sleep, 'assignments': val_assign, 'social': val_social,
                    'score': s.predicted_score, 'risk': s.risk_level, 'cluster': cluster_val
                })

            context = {
                'bulk_results': results,
                'student_data_json': student_data_dash, # Keep charts working
                'student_data_list': student_data_dash,
                'show_bulk_modal': True # Trigger frontend display
            }
            return render(request, 'dashboard/teacher_dashboard.html', context)
            
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")
            return redirect('teacher_dashboard')

    return redirect('teacher_dashboard')
