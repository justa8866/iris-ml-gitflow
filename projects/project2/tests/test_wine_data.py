from projects.project2.src.wine_data import load_wine_frame


def test_load_wine_frame_has_expected_shape_and_features():
    frame = load_wine_frame()

    assert frame.shape == (178, 14)
    assert frame.columns[0] == "alcohol"
    assert frame.columns[-1] == "target"


def test_load_wine_frame_has_three_complete_classes():
    frame = load_wine_frame()

    assert frame["target"].nunique() == 3
    assert frame["target"].value_counts().sum() == 178
    assert frame.isna().sum().sum() == 0
