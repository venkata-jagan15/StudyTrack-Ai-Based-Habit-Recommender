
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_insight.settings')
django.setup()

from django.urls import get_resolver, reverse

def check_urls():
    print("Checking URL Patterns via reverse()...")
    try:
        url = reverse('bulk_analyze')
        print(f"SUCCESS: 'bulk_analyze' found! URL: {url}")
    except Exception as e:
        print(f"FAIL: Reverse lookup failed: {e}")
        
    # Also check if 'teacher_dashboard' exists to compare
    try:
        url2 = reverse('teacher_dashboard')
        print(f"INFO: 'teacher_dashboard' found! URL: {url2}")
    except:
        print("INFO: 'teacher_dashboard' NOT found.")
if __name__ == "__main__":
    check_urls()
