import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from src.data import load_iris_frame
from src.model import build_baseline_pipeline, evaluate_model, train_baseline


def test_baseline_pipeline_scales_and_classifies():
    pipeline = build_baseline_pipeline()

    assert isinstance(pipeline.named_steps["standardscaler"], StandardScaler)
    assert isinstance(pipeline.named_steps["logisticregression"], LogisticRegression)


def test_training_uses_stratified_holdout_and_meets_baseline_accuracy():
    frame = load_iris_frame()
    model, X_test, y_test = train_baseline(frame)

    assert len(X_test) == 30
    assert y_test.value_counts().to_dict() == {
        "setosa": 10,
        "versicolor": 10,
        "virginica": 10,
    }
    metrics = evaluate_model(model, X_test, y_test)
    assert metrics["accuracy"] >= 0.9
    assert metrics["balanced_accuracy"] >= 0.9


def test_training_requires_species_target():
    with pytest.raises(ValueError, match="species"):
        train_baseline(pd.DataFrame({"measurement": [1.0, 2.0]}))
