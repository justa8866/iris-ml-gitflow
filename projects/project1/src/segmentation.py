import pandas as pd

from shared.data_validation import require_columns, require_no_missing_values


def segment_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of customers with rule-based segment labels."""
    require_columns(customers, ["annual_spend_pln", "orders_per_year"])
    require_no_missing_values(customers)

    segments = pd.Series("Occasional", index=customers.index, dtype="object")
    regular_mask = (customers["annual_spend_pln"] >= 2000) | (
        customers["orders_per_year"] >= 8
    )
    vip_mask = (customers["annual_spend_pln"] >= 4000) & (
        customers["orders_per_year"] >= 12
    )
    segments.loc[regular_mask] = "Regular"
    segments.loc[vip_mask] = "VIP"
    return customers.assign(segment=segments)