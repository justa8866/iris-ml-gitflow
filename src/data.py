import pandas as pd
from sklearn.datasets import load_iris


def load_iris_frame() -> pd.DataFrame:
    """Return the built-in Iris dataset with readable species labels."""
    iris = load_iris(as_frame=True)
    frame = iris.data.copy()
    frame["species"] = iris.target.map(dict(enumerate(iris.target_names)))
    return frame