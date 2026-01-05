import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_study_insight.settings')
django.setup()

def check_dash_tables():
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES LIKE 'dashboard_%'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Dashboard tables found: {tables}")
        
        expected = [
            'dashboard_userprofile',
            'dashboard_habitlog',
            'dashboard_subjectgrade',
            'dashboard_weeklytestscore',
            'dashboard_teacherfeedback',
            'dashboard_airecommendation'
        ]
        
        missing = [t for t in expected if t not in tables]
        if missing:
            print(f"MISSING TABLES: {missing}")
        else:
            print("All dashboard tables present.")

if __name__ == "__main__":
    check_dash_tables()
