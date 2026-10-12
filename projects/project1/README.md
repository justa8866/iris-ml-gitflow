# Project 1: Customer Segmentation

A small customer segmentation simulation based on annual spend and order frequency.

## Structure

```text
data/       Local customer datasets (ignored)
notebooks/  Exploratory analysis notebooks
src/        Segmentation code
tests/      Unit tests
models/     Generated model artifacts (ignored)
```

## Input schema

The input dataframe must contain `annual_spend_pln` and `orders_per_year` with no missing values.

## Rules

- `VIP`: annual spend is at least 4000 PLN and the customer places at least 12 orders per year.
- `Regular`: annual spend is at least 2000 PLN or the customer places at least 8 orders per year.
- `Occasional`: all other customers.

Use `segment_customers` from `src/segmentation.py`. Input validation is provided by the shared package.