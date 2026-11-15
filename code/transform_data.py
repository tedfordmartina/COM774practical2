
import pandas as pd


def transform_data(prepared_df):

    # Work on a copy
    df = prepared_df.copy()

    # Handle Apache placeholders
    df["user_agent"] = df["user_agent"].replace("-", "")
    df["referrer"] = df["referrer"].replace("-", "")

    # Convert numerical fields
    df["status_code"] = pd.to_numeric(
        df["status_code"], errors="coerce"
    )

    df["response_bytes"] = pd.to_numeric(
        df["response_bytes"], errors="coerce"
    )

    # Convert timestamps
    dates = pd.to_datetime(
        df["timestamp"],
        format="%d/%b/%Y:%H:%M:%S %z",
        errors="coerce",
        utc=True
    )

    df["timestamp"] = dates

    #Five new features
    df["hour"] = dates.dt.hour
    df["day_of_week"] = dates.dt.dayofweek

    # Features URL features
    df["url_length"] = df["url_path"].str.len()

    df["has_query_string"] = (
        df["url_path"].str.contains("?", regex=False)
    ).astype(int)

    df["user_agent_length"] = df["user_agent"].str.len()

    # Display results
    print("\n===== TRANSFORMATION RESULTS =====")
    print("Total records:", len(df))
    print("Total columns:", len(df.columns))
    print("Invalid timestamps:", dates.isna().sum())

    return df
