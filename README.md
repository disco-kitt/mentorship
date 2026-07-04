# Mentorship Matching Prototype

A GitHub-safe, anonymized mentorship matching prototype for matching students with alumni or mentors using configurable, explainable scoring criteria.

## What this project does

- Loads student and alumni CSV files
- Cleans and validates expected columns
- Scores every possible student/mentor pair
- Explains why each score was assigned
- Creates capacity-aware matches based on mentor availability
- Exports match results to CSV

## Repository structure

```text
mentorship_matching_v2/
├── notebooks/
│   └── mentorship_matching_demo.ipynb
├── sample_data/
│   ├── students.csv
│   └── alumni.csv
├── src/
│   ├── config.py
│   ├── loader.py
│   ├── preprocessing.py
│   ├── scoring.py
│   ├── matching.py
│   └── reporting.py
├── outputs/
├── tests/
├── requirements.txt
└── README.md
```

## Data privacy

This repository contains only synthetic sample data. Do not commit real student, alumni, mentor, or institutional survey exports. Keep real files in a local `private_data/` folder, which is ignored by Git.

## Required student columns

- Student ID
- First Name
- Last Name
- Email
- Career Interest
- Industry Interest

Optional but recommended:

- Program
- Graduation Year
- Location
- Preferred Meeting
- Gender Identity
- First-Generation
- International Student
- Mentor Preferences

## Required alumni columns

- Alumni ID
- First Name
- Last Name
- Email
- Functional Expertise
- Industry
- Max Mentees

Optional but recommended:

- Employer
- Title
- Location
- Meeting Preference
- LGBTQ+ Mentor
- First-Generation

## How to run

Install dependencies:

```bash
pip install -r requirements.txt
```

Then open:

```text
notebooks/mentorship_matching_demo.ipynb
```

The notebook supports two workflows:

1. Use the included synthetic sample CSVs.
2. Upload your own CSVs in Google Colab.

## Customizing scoring

Edit `src/config.py` to change the scoring weights.

```python
WEIGHTS = {
    "career_function": 30,
    "industry": 25,
    "location": 10,
    "meeting_preference": 10,
    "first_generation": 10,
    "identity_affinity": 5,
    "preference_keywords": 10,
}
```
