from collections.abc import Iterable

import pandas as pd


def require_columns(
    frame: pd.DataFrame,
    required_columns: Iterable[str],
) -> pd.DataFrame:
    """Return frame when all requested columns are present."""
    missing_columns = sorted(set(required_columns).difference(frame.columns))
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing}")
    return frame


def require_no_missing_values(frame: pd.DataFrame) -> pd.DataFrame:
    """Return frame when every column contains complete values."""
    missing_columns = frame.columns[frame.isna().any()].tolist()
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing values found in columns: {missing}")
    return frame
