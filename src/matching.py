"""Capacity-aware matching."""

from __future__ import annotations

from collections import defaultdict

import pandas as pd

from .scoring import score_all_pairs


def assign_matches(students: pd.DataFrame, alumni: pd.DataFrame) -> pd.DataFrame:
    """Assign each student to one mentor while respecting mentor capacity.

    This uses a transparent greedy strategy: strongest remaining pair first, then
    capacity is decremented. It is intentionally easy for nontechnical program
    staff to audit. For very large cohorts, replace this with an optimization
    solver while keeping the same score table interface.
    """
    scored = score_all_pairs(students, alumni)
    scored = scored.sort_values("Score", ascending=False).reset_index(drop=True)

    capacity = dict(zip(alumni["Alumni ID"], alumni["Max Mentees"]))
    assigned_students = set()
    rows = []

    for _, row in scored.iterrows():
        student_id = row["Student ID"]
        mentor_id = row["Alumni ID"]
        if student_id in assigned_students:
            continue
        if capacity.get(mentor_id, 0) <= 0:
            continue
        rows.append(row.to_dict())
        assigned_students.add(student_id)
        capacity[mentor_id] -= 1

    matches = pd.DataFrame(rows)

    # Add unmatched students for administrator review.
    unmatched = set(students["Student ID"]) - assigned_students
    if unmatched:
        unmatched_rows = []
        for student_id in sorted(unmatched):
            student = students.loc[students["Student ID"] == student_id].iloc[0]
            unmatched_rows.append({
                "Student ID": student_id,
                "Student Name": f"{student.get('First Name', '')} {student.get('Last Name', '')}".strip(),
                "Alumni ID": "",
                "Mentor Name": "UNMATCHED",
                "Score": 0,
                "Rationale": "No mentor capacity remained",
            })
        matches = pd.concat([matches, pd.DataFrame(unmatched_rows)], ignore_index=True)

    return matches.sort_values(["Mentor Name", "Student Name"]).reset_index(drop=True)
