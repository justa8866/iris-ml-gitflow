# Iris ML Git Flow

[![Tests Passing](https://github.com/justa8866/iris-ml-gitflow/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/justa8866/iris-ml-gitflow/actions/workflows/test.yml)

A reproducible classification project using the Iris toy dataset bundled with scikit-learn. The project demonstrates exploratory data analysis, a baseline classifier, and a Git Flow release process.

## Dataset

The project loads the built-in Iris dataset through `sklearn.datasets.load_iris`; no external download or dataset file is required. It contains 150 samples, four flower measurements, and three species labels. The `data/` directory is reserved for local data and is excluded from Git.

## Project structure

```text
data/                 Local datasets (ignored)
models/               Trained model artifacts (ignored)
notebooks/            Exploratory analysis
src/                  Reusable loading, analysis, and training code
tests/                Automated checks
requirements.txt      Python dependencies
```

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS or Linux, activate the environment with `source .venv/bin/activate`.

## Run

- Open `notebooks/01_iris_eda.ipynb` to inspect class balance, summary statistics, and feature relationships.
- Run `python -m src.train` to train and evaluate the baseline model. The fitted model is saved under `models/` and is not tracked by Git.
- Run `pytest` to execute the automated checks.

The training workflow uses a stratified train/test split with a fixed random seed and a scaled logistic-regression pipeline.

## Git Flow

`main` contains releases. `develop` integrates completed work. Feature branches are merged into `develop` through pull requests, then `develop` is merged into `main` for a tagged release.
