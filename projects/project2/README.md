# Project 2: Wine Classification

A compact classification project using the Wine dataset bundled with scikit-learn.

## Structure

```text
data/       Local datasets (ignored)
notebooks/  Exploratory analysis notebooks
src/        Dataset loading and model code
tests/      Unit tests
models/     Generated model artifacts (ignored)
```

## Dataset

`src/wine_data.py` loads 178 samples with 13 numeric measurements and a three-class target through `sklearn.datasets.load_wine`. The dataset is bundled with scikit-learn, so no files are downloaded or stored in this project.

The loader uses validation functions from the monorepo's `shared/` package.