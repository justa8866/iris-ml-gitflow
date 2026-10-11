import pandas as pd
import pytest

from src.eda import species_counts, summarize_by_species


def test_species_counts_returns_sorted_counts():
    frame = pd.DataFrame({"species": ["virginica", "setosa", "setosa"]})

    counts = species_counts(frame)

    assert counts.to_dict() == {"setosa": 2, "virginica": 1}


def test_summary_calculates_feature_statistics_by_species():
    frame = pd.DataFrame(
        {
            "species": ["setosa", "setosa", "versicolor"],
            "measurement": [1.0, 3.0, 10.0],
        }
    )

    summary = summarize_by_species(frame)

    assert summary.loc["setosa", ("measurement", "mean")] == 2.0
    assert summary.loc["versicolor", ("measurement", "mean")] == 10.0


@pytest.mark.parametrize("helper", [species_counts, summarize_by_species])
def test_eda_helpers_require_species_column(helper):
    with pytest.raises(ValueError, match="species"):
        helper(pd.DataFrame({"measurement": [1.0, 2.0]}))
