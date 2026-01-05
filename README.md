# StudyTrack AI - Student Study Habit Recommender System 

This project is the backend implementation for **StudyTrack**, an AI-powered platform designed to analyze student study habits and predict academic performance. This milestone focuses on the Django server integration with Machine Learning models.

## Features

- **User Authentication**: Separate login and registration flows for **Students** and **Teachers**.
- **Student Dashboard**: 
    - Log daily study habits (Study Hours, Sleep Hours, Social Media Usage, Assignments).
    - View AI-predicted test scores based on habits.
    - Receive personalized recommendations (e.g., "Improve sleep schedule").
- **Teacher Dashboard**:
    - View analytics for all students.
    - see risk levels (Low, Medium, High).
    - **Bulk Analysis**: Upload CSV files for batch prediction of student scores and clustering.
- **Machine Learning Integration**:
    - **Linear Regression**: Predicts student scores based on input features.
    - **K-Means Clustering**: Segments students into behavioral clusters (e.g., "Hardworking", "Sleep Deprived").

## Prerequisites

Ensure you have the following installed:
- Python 3.8+
- MySQL Server

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pandas scikit-learn  # Required for ML modules
   ```

4. **Database Setup**:
   - Ensure MySQL is running.
   - Update `DATABASES` in `ai_study_insight/settings.py` with your MySQL credentials.
   - Run migrations:
     ```bash
     python manage.py migrate
     ```

5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the application at `http://127.0.0.1:8000/`.
- **Register**: Create a Student or Teacher account.
- **Student**: Log study data to get predictions.
- **Teacher**: Monitor student progress or use the "Bulk Analyze" feature with a CSV file.

## Project Structure

- `ai_study_insight/`: Core Django project settings.
- `dashboard/`: Main application logic.
    - `models.py`: Database schema (UserProfile, HabitLog, etc.).
    - `views.py`: Request handlers for dashboards.
    - `ml_utils.py`: Machine Learning logic for prediction and clustering.
- `templates/`: HTML templates for the frontend.
- `static/`: CSS and JavaScript files.

## Troubleshooting

- **KeyError: 'Test_Score'**: If you encounter this during bulk analysis, ensure your CSV file has a `Test_Score` column, or `Attendance_Percentage` (which will be treated as the score).
