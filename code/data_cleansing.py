import pandas as pd
from pathlib import Path


def prepare_data(input_filename):

    # Load parsed Apache log CSV
    df = pd.read_csv(
        input_filename,
        dtype=str,
        keep_default_na=False
    )

    # Create a copy
    features = df.copy()

    # Remove non-informative columns
    features = features.drop(
        columns=["identity", "username"]
    )

    # Check dataset
    print("\nTotal records:", len(features))
    print("Total columns:", len(features.columns))
    print("Parsing errors:", (features["parse_error"] != "").sum())

    # Check missing values
    print("\nMissing or unavailable values:")
    print(features.isin(["", "-"]).sum())

    # Check attack labels
    print("\nAttack labels:")
    print(features["label_attack"].value_counts())

    return features


