# History Cleanup Exercise

## Dataset workflow

- Use the built-in Iris dataset so the workflow is reproducible without downloading files.
- Keep the feature columns and species target in one labelled table for analysis.
- Check class balance before comparing results between species.
- Fix the random seed when splitting data so runs can be compared consistently.

## Baseline model

- Keep scaling inside the classifier pipeline to prevent test-set leakage.
- Report accuracy and balanced accuracy together when classes may be uneven.
- Inspect the confusion matrix to identify species-level errors.
