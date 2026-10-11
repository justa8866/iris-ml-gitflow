import pandas as pd


def species_counts(frame: pd.DataFrame) -> pd.Series:
    """Return the number of samples for each species."""
    if "species" not in frame.columns:
        raise ValueError("frame must contain a 'species' column")
    return frame["species"].value_counts().sort_index()


def summarize_by_species(frame: pd.DataFrame) -> pd.DataFrame:
    """Return mean and standard deviation for numeric features by species."""
    if "species" not in frame.columns:
        raise ValueError("frame must contain a 'species' column")

    numeric_columns = frame.select_dtypes(include="number").columns
    summary = frame.groupby("species", observed=True)[numeric_columns].agg(
        ["mean", "std"]
    )
    return summary.round(2)
