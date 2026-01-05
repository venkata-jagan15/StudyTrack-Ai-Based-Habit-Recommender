
import os
import django
import sys
from django.test import RequestFactory
import pandas as pd
from io import StringIO

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_insight.settings')
django.setup()

from dashboard.views import bulk_analyze
from django.contrib.auth.models import User
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

def verify_bulk_analysis():
    print("Verifying Bulk Analysis Logic with Client...")
    
    # Create valid CSV content
    csv_content = """Study_Hours,Sleep_Hours,Assignments_Completed,Social_Media_Hours
5,7,8,2
8,8,10,1
2,4,2,5
"""
    # Create the file (needs to be treated as file for Client)
    csv_file = SimpleUploadedFile("test_upload.csv", csv_content.encode('utf-8'), content_type="text/csv")
    
    client = Client()
    # Create and login user if needed (assuming teacher dashboard might enforce it, though view might not)
    user, _ = User.objects.get_or_create(username="test_teacher_bulk")
    if not user.check_password("password"):
        user.set_password("password")
        user.save()
    client.force_login(user)
    
    try:
        response = client.post('/bulk_analyze/', {'csv_file': csv_file}, follow=True)
        print(f"Response Code: {response.status_code}")
        
        content = response.content.decode('utf-8')
        # Check for error messages
        if "Please upload a valid CSV file" in content:
            print("FAIL: Invalid file error.")
        elif "CSV must contain columns" in content:
            print("FAIL: Column mismatch error.")
        elif "Error processing file" in content:
            print("FAIL: Processing error.")
            
        if "Bulk Analysis Results" in content and "Sleep Focus" in content:
            print("SUCCESS: Bulk analysis processed and results displayed.")
        else:
             print("FAIL: Results table not found. Dump of messages:")
             from django.contrib.messages import get_messages
             msgs = list(get_messages(response.wsgi_request))
             for m in msgs: print(f" - {m}")
            
    except Exception as e:
        print(f"FAIL: Exception during execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_bulk_analysis()
