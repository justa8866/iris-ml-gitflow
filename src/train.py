from pathlib import Path

import joblib

from src.data import load_iris_frame
from src.model import evaluate_model, train_baseline


def main() -> None:
    """Train, evaluate, and persist the baseline classifier."""
    frame = load_iris_frame()
    model, X_test, y_test = train_baseline(frame)
    metrics = evaluate_model(model, X_test, y_test)

    model_path = Path("models/iris_logistic_regression.joblib")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    print(f"Accuracy: {metrics['accuracy']:.3f}")
    print(f"Balanced accuracy: {metrics['balanced_accuracy']:.3f}")
    print(f"Saved model to {model_path}")


if __name__ == "__main__":
    main()