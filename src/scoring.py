"""Explainable mentor/student scoring."""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

import pandas as pd

from .config import WEIGHTS


def _contains_overlap(left: str, right: str) -> bool:
    if not left or not right:
        return False
    return left in right or right in left


def _keyword_overlap(text: str, comparison_fields: List[str]) -> List[str]:
    if not text:
        return []
    tokens = {t for t in re.split(r"[^a-z0-9+]+", text.lower()) if len(t) >= 4}
    comparison = " ".join(comparison_fields).lower()
    return sorted(token for token in tokens if token in comparison)


def score_pair(student: pd.Series, alumni: pd.Series, weights: Dict[str, int] | None = None) -> Tuple[int, List[str]]:
    """Score one student/alumni pairing and return score plus rationale."""
    weights = weights or WEIGHTS
    score = 0
    reasons: List[str] = []

    if _contains_overlap(student.get("_Career Interest", ""), alumni.get("_Functional Expertise", "")):
        score += weights["career_function"]
        reasons.append("Career interest aligns with mentor functional expertise")

    if _contains_overlap(student.get("_Industry Interest", ""), alumni.get("_Industry", "")):
        score += weights["industry"]
        reasons.append("Shared industry interest")

    if student.get("_Location", "") and student.get("_Location", "") == alumni.get("_Location", ""):
        score += weights["location"]
        reasons.append("Same location")

    if student.get("_Preferred Meeting", "") and student.get("_Preferred Meeting", "") == alumni.get("_Meeting Preference", ""):
        score += weights["meeting_preference"]
        reasons.append("Compatible meeting preference")

    if student.get("_First-Generation", "") == "yes" and alumni.get("_First-Generation", "") == "yes":
        score += weights["first_generation"]
        reasons.append("Shared first-generation experience")

    gender = student.get("_Gender Identity", "")
    if any(term in gender for term in ["non-binary", "trans", "queer", "lgbtq"]) and alumni.get("_LGBTQ+ Mentor", "") == "yes":
        score += weights["identity_affinity"]
        reasons.append("Student requested or may benefit from LGBTQ+ mentor affinity")

    keywords = _keyword_overlap(
        student.get("_Mentor Preferences", ""),
        [
            alumni.get("_Industry", ""),
            alumni.get("_Functional Expertise", ""),
            str(alumni.get("Title", "")),
            str(alumni.get("Employer", "")),
        ],
    )
    if keywords:
        score += weights["preference_keywords"]
        reasons.append(f"Mentor profile overlaps with preference keywords: {', '.join(keywords)}")

    return min(score, 100), reasons


def score_all_pairs(students: pd.DataFrame, alumni: pd.DataFrame, weights: Dict[str, int] | None = None) -> pd.DataFrame:
    """Create a long-form score table for every student/mentor pair."""
    rows = []
    for _, student in students.iterrows():
        for _, mentor in alumni.iterrows():
            score, reasons = score_pair(student, mentor, weights=weights)
            rows.append({
                "Student ID": student["Student ID"],
                "Student Name": f"{student.get('First Name', '')} {student.get('Last Name', '')}".strip(),
                "Alumni ID": mentor["Alumni ID"],
                "Mentor Name": f"{mentor.get('First Name', '')} {mentor.get('Last Name', '')}".strip(),
                "Score": score,
                "Rationale": "; ".join(reasons) if reasons else "No major scoring criteria matched",
            })
    return pd.DataFrame(rows).sort_values(["Student ID", "Score"], ascending=[True, False])
