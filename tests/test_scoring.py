import pandas as pd

from src.preprocessing import preprocess_alumni, preprocess_students
from src.scoring import score_pair


def test_score_pair_returns_score_and_reasons():
    student = preprocess_students(pd.DataFrame([{
        "Student ID":"S1", "First Name":"Test", "Last Name":"Student", "Email":"student@example.edu",
        "Career Interest":"Data Science", "Industry Interest":"Healthcare", "Location":"San Diego, CA",
        "Preferred Meeting":"Hybrid", "Gender Identity":"Woman", "First-Generation":"No",
        "International Student":"Yes", "Mentor Preferences":"Healthcare analytics"
    }])).iloc[0]
    mentor = preprocess_alumni(pd.DataFrame([{
        "Alumni ID":"A1", "First Name":"Test", "Last Name":"Mentor", "Email":"mentor@example.org",
        "Functional Expertise":"Data Science", "Industry":"Healthcare", "Location":"San Diego, CA",
        "Meeting Preference":"Hybrid", "Max Mentees":1, "LGBTQ+ Mentor":"No", "First-Generation":"No"
    }])).iloc[0]
    score, reasons = score_pair(student, mentor)
    assert score > 0
    assert reasons
