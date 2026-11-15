
import pandas as pd
from sklearn.preprocessing import StandardScaler


def encoding_scaling(df):
    """
    Demonstrate categorical encoding and numerical scaling
    for COM774 CW1.

    This is an exploratory demonstration only.
    No machine-learning model is trained.
    """

    # Work on a copy of the cleaned data
    data = df.copy()

    # 1. Select the features to demonstrate
    categorical_columns = [
        "http_method",
        "status_code"
    ]

    numerical_columns = [
        "url_length",
        "response_bytes",
        "user_agent_length"
    ]

    # 2. Show the original data
    print("\nBEFORE PREPROCESSING")
    print(data[categorical_columns + numerical_columns].head())

    # 3. One-hot encode categorical features
    encoded = pd.get_dummies(
        data[categorical_columns].astype(str),
        dtype=int
    )

    # 4. Standardise numerical features
    scaler = StandardScaler()

    scaled = pd.DataFrame(
        scaler.fit_transform(data[numerical_columns]),
        columns=numerical_columns,
        index=data.index
    )

    # 5. Combine the transformed features
    processed = pd.concat(
        [encoded, scaled],
        axis=1
    )

    # 6. Show the results
    print("\nAFTER PREPROCESSING")
    print(processed.head().round(3))

    print("\nORIGINAL FEATURE COUNT:",
          len(categorical_columns + numerical_columns))

    print("TRANSFORMED FEATURE COUNT:",
          processed.shape[1])

    print("\nENCODED COLUMNS:")
    print(encoded.columns.tolist())

    return processed

