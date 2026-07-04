from pathlib import Path

from src.loader import load_sample_data
from src.preprocessing import preprocess_alumni, preprocess_students
from src.matching import assign_matches


def test_assign_matches_sample_data():
    root = Path(__file__).resolve().parents[1]
    students, alumni = load_sample_data(root)
    matches = assign_matches(preprocess_students(students), preprocess_alumni(alumni))
    assert len(matches) == len(students)
    assert "Score" in matches.columns
