"""Cleaning and validation helpers."""

from __future__ import annotations

import re
from typing import Iterable

import pandas as pd

from .config import ALUMNI_REQUIRED_COLUMNS, STUDENT_REQUIRED_COLUMNS


def normalize_text(value: object) -> str:
    """Normalize user-entered survey text for matching."""
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def validate_columns(df: pd.DataFrame, required: Iterable[str], label: str) -> None:
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"{label} file is missing required columns: {missing}")


def preprocess_students(students: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the students table."""
    students = students.copy()
    validate_columns(students, STUDENT_REQUIRED_COLUMNS, "Student")
    text_columns = [
        "Career Interest",
        "Industry Interest",
        "Location",
        "Preferred Meeting",
        "Gender Identity",
        "First-Generation",
        "International Student",
        "Mentor Preferences",
    ]
    for column in text_columns:
        if column not in students.columns:
            students[column] = ""
        students[f"_{column}"] = students[column].map(normalize_text)
    return students


def preprocess_alumni(alumni: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the alumni/mentors table."""
    alumni = alumni.copy()
    validate_columns(alumni, ALUMNI_REQUIRED_COLUMNS, "Alumni")
    text_columns = [
        "Industry",
        "Functional Expertise",
        "Location",
        "Meeting Preference",
        "LGBTQ+ Mentor",
        "First-Generation",
    ]
    for column in text_columns:
        if column not in alumni.columns:
            alumni[column] = ""
        alumni[f"_{column}"] = alumni[column].map(normalize_text)

    alumni["Max Mentees"] = pd.to_numeric(alumni["Max Mentees"], errors="coerce").fillna(1).astype(int)
    alumni["Max Mentees"] = alumni["Max Mentees"].clip(lower=0)
    return alumni
