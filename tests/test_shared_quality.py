import pandas as pd
from shared.data_validation import require_no_missing_values


def test_complete_frame_is_returned():
    frame = pd.DataFrame({"value": [1, 2]})
    assert require_no_missing_values(frame) is frame
