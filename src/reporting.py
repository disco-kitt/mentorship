"""Reporting and export helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_matches(matches: pd.DataFrame, output_path: str | Path = "outputs/matches.csv") -> Path:
    """Export final matches to CSV and return the written path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    matches.to_csv(path, index=False)
    return path
