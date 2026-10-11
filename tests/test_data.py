from src.data import load_iris_frame


def test_load_iris_frame_has_expected_features_and_target():
    frame = load_iris_frame()

    assert frame.shape == (150, 5)
    assert list(frame.columns) == [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
        "species",
    ]
    assert frame.isna().sum().sum() == 0


def test_load_iris_frame_has_balanced_species_labels():
    frame = load_iris_frame()

    assert frame["species"].value_counts().to_dict() == {
        "setosa": 50,
        "versicolor": 50,
        "virginica": 50,
    }
