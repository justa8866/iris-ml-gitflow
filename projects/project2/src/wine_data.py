import pandas as pd
from sklearn.datasets import load_wine

from shared.data_validation import require_columns, require_no_missing_values


def load_wine_frame() -> pd.DataFrame:
    """Return the built-in Wine dataset with readable class labels."""
    wine = load_wine(as_frame=True)
    frame = wine.data.copy()
    frame["target"] = wine.target.map(dict(enumerate(wine.target_names)))
    require_columns(frame, ["alcohol", "malic_acid", "target"])
    require_no_missing_values(frame)
    return frame
