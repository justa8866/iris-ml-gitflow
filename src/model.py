import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


def build_baseline_pipeline() -> Pipeline:
    """Build a scaled logistic-regression classifier."""
    return make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000, random_state=42),
    )


def train_baseline(
    frame: pd.DataFrame,
) -> tuple[Pipeline, pd.DataFrame, pd.Series]:
    """Train a baseline model and return it with the held-out test split."""
    if "species" not in frame.columns:
        raise ValueError("frame must contain a 'species' target column")

    features = frame.drop(columns="species")
    target = frame["species"]
    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target,
    )

    model = build_baseline_pipeline()
    model.fit(X_train, y_train)
    return model, X_test, y_test


def evaluate_model(
    model: Pipeline,
    features: pd.DataFrame,
    target: pd.Series,
) -> dict[str, float]:
    """Return accuracy metrics for a fitted classifier."""
    predictions = model.predict(features)
    return {
        "accuracy": float(accuracy_score(target, predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(target, predictions)),
    }
