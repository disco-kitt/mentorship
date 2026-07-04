"""Data loading helpers for sample, local, and Google Colab CSV workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import pandas as pd


def _read_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    return pd.read_csv(path)


def load_sample_data(base_dir: str | Path = ".") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load bundled sample student and alumni CSVs.

    Expected paths:
        sample_data/students.csv
        sample_data/alumni.csv
    """
    base = Path(base_dir)
    students = _read_csv(base / "sample_data" / "students.csv")
    alumni = _read_csv(base / "sample_data" / "alumni.csv")
    return students, alumni


def load_csvs(student_csv: str | Path, alumni_csv: str | Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load user-supplied student and alumni CSVs."""
    return _read_csv(student_csv), _read_csv(alumni_csv)


def load_from_colab_upload() -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """Prompt for two CSV uploads in Google Colab.

    Returns None outside Colab. In Colab, upload exactly two files. The function
    guesses which CSV is students vs alumni by looking for expected column names.
    """
    try:
        from google.colab import files  # type: ignore
    except Exception:
        return None

    uploaded = files.upload()
    if len(uploaded) != 2:
        raise ValueError("Please upload exactly two CSV files: one students file and one alumni/mentors file.")

    dataframes = {name: pd.read_csv(name) for name in uploaded.keys()}

    student_name = None
    alumni_name = None
    for name, df in dataframes.items():
        columns = {str(c).strip().lower() for c in df.columns}
        if {"student id", "career interest"}.issubset(columns) or "graduation year" in columns:
            student_name = name
        if {"alumni id", "functional expertise"}.issubset(columns) or "max mentees" in columns:
            alumni_name = name

    if student_name is None or alumni_name is None or student_name == alumni_name:
        names = list(dataframes.keys())
        raise ValueError(
            "Could not confidently identify the student and alumni CSVs. "
            f"Uploaded files: {names}. Make sure they include clear ID and interest/expertise columns."
        )

    return dataframes[student_name], dataframes[alumni_name]
