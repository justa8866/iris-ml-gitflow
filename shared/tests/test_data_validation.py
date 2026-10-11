import pandas as pd
import pytest

from shared.data_validation import require_columns, require_no_missing_values


def test_require_columns_returns_original_frame_when_valid():
    frame = pd.DataFrame({"feature": [1, 2], "target": ["a", "b"]})

    assert require_columns(frame, ["feature", "target"]) is frame


def test_require_columns_reports_missing_columns():
    frame = pd.DataFrame({"feature": [1, 2]})

    with pytest.raises(ValueError, match="target"):
        require_columns(frame, ["target"])


def test_require_no_missing_values_reports_incomplete_columns():
    frame = pd.DataFrame({"feature": [1.0, None]})

    with pytest.raises(ValueError, match="feature"):
        require_no_missing_values(frame)