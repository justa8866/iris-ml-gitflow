import pandas as pd
import pytest

from projects.project1.src.segmentation import segment_customers


def test_segment_customers_applies_thresholds_without_mutating_input():
    customers = pd.DataFrame(
        {
            "annual_spend_pln": [5000, 2500, 900, 5000],
            "orders_per_year": [12, 4, 2, 7],
        }
    )

    result = segment_customers(customers)

    assert result["segment"].tolist() == ["VIP", "Regular", "Occasional", "Regular"]
    assert "segment" not in customers.columns


def test_segment_customers_requires_both_input_columns():
    with pytest.raises(ValueError, match="orders_per_year"):
        segment_customers(pd.DataFrame({"annual_spend_pln": [1000]}))


def test_segment_customers_rejects_missing_values():
    customers = pd.DataFrame(
        {"annual_spend_pln": [1000], "orders_per_year": [None]}
    )

    with pytest.raises(ValueError, match="orders_per_year"):
        segment_customers(customers)