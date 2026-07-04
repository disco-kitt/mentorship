"""Configuration for mentorship matching.

Edit these weights to change how strongly each criterion affects the match score.
The default values are intentionally transparent and easy to explain to program staff.
"""

WEIGHTS = {
    "career_function": 30,
    "industry": 25,
    "location": 10,
    "meeting_preference": 10,
    "first_generation": 10,
    "identity_affinity": 5,
    "preference_keywords": 10,
}

STUDENT_REQUIRED_COLUMNS = [
    "Student ID",
    "First Name",
    "Last Name",
    "Email",
    "Career Interest",
    "Industry Interest",
]

ALUMNI_REQUIRED_COLUMNS = [
    "Alumni ID",
    "First Name",
    "Last Name",
    "Email",
    "Functional Expertise",
    "Industry",
    "Max Mentees",
]
