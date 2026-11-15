



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Project folders
PROJECT = Path(r"C:\COM774_CW1_MT")
OUTPUT = PROJECT / "visuals"
OUTPUT.mkdir(parents=True, exist_ok=True)

# Consistent chart styling
sns.set_theme(style="whitegrid", context="notebook")


def save_chart(filename):
    plt.tight_layout()
    plt.savefig(OUTPUT / filename, dpi=300, bbox_inches="tight")
    plt.close()


def plot_status_codes(df):
    counts = df["status_code"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 5))

    bars = ax.barh(
        counts.index.astype(str),
        counts.values,
        color="#376A9B"
    )

    ax.bar_label(bars, padding=4, fmt="%.0f")
    ax.set_xlim(0, counts.max() * 1.2)

    ax.set_title("HTTP Status Code Distribution", fontweight="bold")
    ax.set_xlabel("Number of Requests")
    ax.set_ylabel("HTTP Status Code")

    save_chart("http_status_codes.png")



def plot_http_methods(df):

    # Count HTTP methods, including blank values
    counts = (
        df["http_method"]
        .replace("", "Missing")
        .value_counts()
        .sort_values()
    )

    # Adjust chart height to number of categories
    height = max(5, len(counts) * 0.5)

    fig, ax = plt.subplots(figsize=(12, height))

    # Horizontal bars
    bars = ax.barh(
        counts.index.astype(str),
        counts.values,
        color="#376A9B",
        height=0.65
    )

    # Add exact request counts
    labels = [f"{value:,}" for value in counts.values]
    ax.bar_label(
        bars,
        labels=labels,
        padding=5,
        fontsize=9
    )

    # Leave space for labels at end of bars
    ax.set_xlim(0, counts.max() * 1.18)

    ax.set_title(
        "HTTP Method Distribution",
        fontsize=15,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel("Number of Requests", fontsize=11)
    ax.set_ylabel("HTTP Method", fontsize=11)

    # Grid lines
    ax.grid(axis="x", linestyle="--", alpha=0.25)
    ax.grid(axis="y", visible=False)
    ax.set_axisbelow(True)

    # Remove unnecessary borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    plt.savefig(
        OUTPUT / "http_methods.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()



def plot_attack_labels(df):
    counts = df["label_attack"].value_counts()

    # Overall distribution
    fig, ax = plt.subplots(figsize=(10, 5))

    bars = ax.barh(
        counts.index.astype(str),
        counts.values,
        color="#168B87"
    )

    ax.bar_label(bars, padding=4, fmt="%.0f")
    ax.set_xlim(0, counts.max() * 1.2)

    ax.set_title("Attack Label Distribution", fontweight="bold")
    ax.set_xlabel("Number of Records")
    ax.set_ylabel("Original Attack Label")

    save_chart("attack_labels.png")

    # Detailed distribution without label 0
    attack_counts = counts.drop("0", errors="ignore").sort_values()

    if not attack_counts.empty:
        fig, ax = plt.subplots(figsize=(10, 5))

        bars = ax.barh(
            attack_counts.index.astype(str),
            attack_counts.values,
            color="#168B87"
        )

        ax.bar_label(bars, padding=4, fmt="%.0f")
        ax.set_xlim(0, max(attack_counts.max() * 1.2, 1))

        ax.set_title(
            "Non-Zero Attack Label Distribution",
            fontweight="bold"
        )
        ax.set_xlabel("Number of Records")
        ax.set_ylabel("Attack Label")

        save_chart("attack_labels_detailed.png")



    
def plot_missing_values(df):

    # Exclude columns that should not be included
    excluded = {
        "parse_error",
        "access_data",
        "line_no",
        "label_time",
        "label_attack"
    }

    columns = [c for c in df.columns if c not in excluded]

    # Count missing and unavailable values
    missing = df[columns].apply(
        lambda col: (
            col.isna()
            | col.astype("string").str.strip().isin(["", "-"])
        ).sum()
    )

    # Keep only columns with missing values
    missing = missing[missing > 0].sort_values()

    if missing.empty:
        print("No unavailable values found.")
        return

    # Create the figure
    fig, ax = plt.subplots(figsize=(11, 6))

    # IMPORTANT: Create bars BEFORE adding labels
    bars = ax.barh(
        missing.index,
        missing.values,
        color="#C27A35",
        height=0.65
    )

    # Add labels, positioning small values away from axis
    for bar, value in zip(bars, missing.values):

        if value < 100:
            x_position = 250
        else:
            x_position = bar.get_width() + 120

        ax.text(
            x_position,
            bar.get_y() + bar.get_height() / 2,
            f"{value:,}",
            va="center",
            ha="left",
            fontsize=10
        )

    # Chart formatting
    ax.set_title(
        "Unavailable Values by Column",
        fontsize=15,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel("Number of Records")
    ax.set_ylabel("Column")

    ax.set_xlim(0, missing.max() * 1.2)

    ax.grid(axis="x", linestyle="--", alpha=0.25)
    ax.grid(axis="y", visible=False)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Save and close
    plt.tight_layout()

    plt.savefig(
        OUTPUT / "missing_values.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()



def plot_url_lengths(df):
    if "url_length" in df.columns:
        lengths = pd.to_numeric(
            df["url_length"], errors="coerce"
        ).dropna()
    else:
        lengths = df["url_path"].fillna("").astype(str).str.len()
        lengths = lengths[df["url_path"].fillna("").ne("")]

    if lengths.empty:
        print("No URL lengths available.")
        return

    cutoff = lengths.quantile(0.99)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        lengths[lengths <= cutoff],
        bins=40,
        color="#376A9B",
        edgecolor="white"
    )

    ax.set_title(
        "URL Length Distribution (Up to 99th Percentile)",
        fontweight="bold"
    )
    ax.set_xlabel("URL Length (Characters)")
    ax.set_ylabel("Number of Requests")

    save_chart("url_length_histogram.png")

    print("\nURL length statistics:")
    print("Median:", lengths.median())
    print("99th percentile:", cutoff)
    print("Maximum:", lengths.max())
    print("Records above 99th percentile:", (lengths > cutoff).sum())


def plot_correlation_heatmap(df):

    columns = [
        "status_code",
        "response_bytes",
        "url_length",
        "user_agent_length",
        "hour",
        "day_of_week",
        "has_query_string"
    ]

    # Select available columns
    available = [c for c in columns if c in df.columns]

    # Convert to numeric
    numeric_df = df[available].apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Calculate correlations
    correlations = numeric_df.corr()

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 7))

    sns.heatmap(
        correlations,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        center=0,
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        square=True,
        ax=ax
    )

    ax.set_title(
        "Correlation Between Web Log Features",
        fontsize=15,
        fontweight="bold",
        pad=20
    )

    plt.xticks(rotation=35, ha="right")
    plt.yticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        OUTPUT / "feature_correlation_heatmap.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()



def plot_web_traffic_timeline(df):

    # Convert Apache timestamps into datetime values
    timestamps = pd.to_datetime(
        df["timestamp"],
        format="%d/%b/%Y:%H:%M:%S %z",
        errors="coerce",
        utc=True
    )

    # Count invalid timestamps
    invalid = timestamps.isna().sum()
    print("Invalid timestamps:", invalid)

    # Count requests per hour
    hourly = (
        pd.Series(1, index=timestamps.dropna())
        .resample("h")
        .sum()
    )

    if hourly.empty:
        print("No valid timestamps available.")
        return

    # Calculate a 24-hour moving average
    moving_average = hourly.rolling(
        window=24,
        min_periods=1
    ).mean()

    # Create chart
    fig, ax = plt.subplots(figsize=(13, 6))

    # Hourly traffic
    ax.plot(
        hourly.index,
        hourly.values,
        color="#2563A6",
        linewidth=1.5,
        label="Hourly requests"
    )

    # Shaded area
    ax.fill_between(
        hourly.index,
        hourly.values,
        color="#2563A6",
        alpha=0.15
    )

    # Moving average
    ax.plot(
        moving_average.index,
        moving_average.values,
        color="#D97706",
        linewidth=2,
        label="24-hour moving average"
    )

    # Highlight peak hour
    peak_time = hourly.idxmax()
    peak_count = hourly.max()

    ax.scatter(
        peak_time,
        peak_count,
        color="#DC2626",
        s=55,
        zorder=5
    )

    ax.annotate(
        f"Peak: {peak_count:,} requests",
        xy=(peak_time, peak_count),
        xytext=(10, 15),
        textcoords="offset points",
        fontsize=9
    )

    # Titles and labels
    ax.set_title(
        "Web Traffic Over Time — mail.cup.com",
        fontsize=16,
        fontweight="bold",
        pad=18
    )

    ax.set_xlabel("Date and Time (UTC)")
    ax.set_ylabel("Requests per Hour")

    # Improve appearance
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.grid(axis="x", visible=False)
    ax.legend(frameon=False)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.autofmt_xdate()

    # Save chart
    plt.tight_layout()

    plt.savefig(
        OUTPUT / "web_traffic_timeline.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Web traffic timeline saved!")
    print("Peak hour:", peak_time)
    print("Peak request count:", peak_count)



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def plot_status_codes_by_attack_label(df, output_dir="visuals"):
    """
    Compare HTTP status codes between normal and attack-labelled requests.
    Uses percentages within each label group to account for class imbalance.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Work on a copy so the original dataset is not modified.
    data = df[["status_code", "label_attack"]].copy()

    # Convert status codes to numeric values.
    data["status_code"] = pd.to_numeric(
        data["status_code"], errors="coerce"
    )

    # Label 0 represents normal traffic.
    # Any non-zero attack label represents attack-related traffic.
    data["traffic_type"] = data["label_attack"].apply(
        lambda value: "Normal" if str(value).strip() in ("0", "0.0")
        else "Attack"
    )

    # Remove records with unavailable status codes.
    data = data.dropna(subset=["status_code"])

    # Convert HTTP status codes to integer strings for display.
    data["status_code"] = data["status_code"].astype(int).astype(str)

    # Count status codes within each traffic group.
    counts = pd.crosstab(
        data["status_code"],
        data["traffic_type"]
    )

    # Convert counts to percentages within each group.
    # This is important because normal traffic greatly outnumbers attacks.
    percentages = counts.div(counts.sum(axis=0), axis=1) * 100

    # Ensure both groups appear in a consistent order.
    percentages = percentages.reindex(
        columns=["Normal", "Attack"],
        fill_value=0
    )

    # Sort status codes numerically.
    percentages = percentages.sort_index(
        key=lambda index: index.astype(int)
    )

    # Plot the results.
    ax = percentages.plot(
        kind="bar",
        figsize=(11, 6),
        color=["#39709E", "#A64B67"],
        width=0.75
    )

    ax.set_title(
        "HTTP Status Codes: Normal vs Attack-Labelled Requests",
        fontsize=16,
        fontweight="bold"
    )
    ax.set_xlabel("HTTP Status Code")
    ax.set_ylabel("Percentage of Requests Within Each Group (%)")
    ax.legend(title="Traffic Type")
    ax.tick_params(axis="x", rotation=0)

    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()

    output_file = output_dir / "status_codes_by_attack_label.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved chart: {output_file}")

    # Print a useful summary for the coursework.
    print("\nStatus code percentages by traffic type:")
    print(percentages.round(2))



def plot_attack_feature_correlations(df, output_dir="visuals"):
    
    #Create a correlation heatmap including the binary attack label.
    

    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from pathlib import Path

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = df.copy()

    # Exclude rows without a valid attack label.
    labels = data["label_attack"].fillna("").astype(str).str.strip()

    # Your normal requests use the label "0".
    # Other non-empty labels identify attack types.
    valid_labels = ~labels.isin(["", "nan", "None"])
    data = data.loc[valid_labels].copy()
    labels = labels.loc[valid_labels]

    # Create a binary target: 0 = Normal, 1 = Attack.
    data["is_attack"] = (~labels.isin(["0", "0.0"])).astype(int)

    # Select the engineered numeric features.
    feature_columns = [
        "response_bytes",
        "hour",
        "day_of_week",
        "url_length",
        "has_query_string",
        "user_agent_length",
        "is_attack"
    ]

    correlation_data = data[feature_columns].copy()

    # Convert values to numeric, including Boolean features.
    for column in feature_columns:
        correlation_data[column] = pd.to_numeric(
            correlation_data[column],
            errors="coerce"
        )

    # Calculate Pearson correlations.
    correlation_matrix = correlation_data.corr()

    # Plot the heatmap.
    plt.figure(figsize=(11, 8))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        square=True
    )

    plt.title(
        "Feature Correlations Including Attack Labels",
        fontsize=15,
        fontweight="bold"
    )

    plt.tight_layout()

    output_file = output_dir / "attack_feature_correlation_heatmap.png"

    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved chart: {output_file}")

    # Show correlations specifically with the attack label.
    print("\nFeature correlations with attack label:")
    print(
        correlation_matrix["is_attack"]
        .drop("is_attack")
        .sort_values(ascending=False)
        .round(3)
    )



def plot_user_agent_by_attack_label(df, output_dir="visuals"):
    """
    Compare user-agent lengths and missing user agents
    between normal and attack-labelled requests.
    """

    import pandas as pd
    import matplotlib.pyplot as plt
    from pathlib import Path

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Work on a copy of the processed dataset
    data = df[["user_agent", "label_attack"]].copy()

    # Remove records with unavailable attack labels
    labels = data["label_attack"].fillna("").astype(str).str.strip()
    valid = ~labels.isin(["", "nan", "None"])
    data = data.loc[valid].copy()
    labels = labels.loc[valid]

    # Convert existing labels into Normal or Attack
    data["traffic_type"] = labels.apply(
        lambda value: "Normal" if value in ("0", "0.0") else "Attack"
    )

    # Standardise unavailable user-agent values
    user_agents = data["user_agent"].fillna("").astype(str).str.strip()
    user_agents = user_agents.replace("-", "")

    # Create the two measurements
    data["user_agent_length"] = user_agents.str.len()
    data["missing_user_agent"] = user_agents.eq("")

    # Summarise each group
    summary = data.groupby("traffic_type").agg(
        requests=("user_agent_length", "size"),
        median_length=("user_agent_length", "median"),
        mean_length=("user_agent_length", "mean"),
        missing_count=("missing_user_agent", "sum"),
        missing_percent=("missing_user_agent", "mean")
    )

    summary["missing_percent"] *= 100

    # Calculate lengths again, excluding missing user agents
    present = data.loc[~data["missing_user_agent"]]

    nonmissing_median = present.groupby(
        "traffic_type"
    )["user_agent_length"].median()

    summary["median_length_when_present"] = nonmissing_median

    # Save the results as a CSV
    summary.to_csv(
        output_dir / "user_agent_attack_summary.csv"
    )

    print("\nUSER-AGENT ANALYSIS")
    print(summary.round(2).to_string())

    # Create two charts side by side
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    order = ["Normal", "Attack"]

    # Chart 1: Median length when a user agent is present
    medians = (
        summary["median_length_when_present"]
        .reindex(order)
    )

    axes[0].bar(
        order,
        medians,
        color=["#39709E", "#A64B67"]
    )
    axes[0].set_title("Median User-Agent Length")
    axes[0].set_ylabel("Characters")
    axes[0].set_xlabel("Traffic Type")

    # Chart 2: Percentage with missing user agents
    missing = summary["missing_percent"].reindex(order)

    axes[1].bar(
        order,
        missing,
        color=["#39709E", "#A64B67"]
    )
    axes[1].set_title("Missing User-Agent Values")
    axes[1].set_ylabel("Percentage of Requests (%)")
    axes[1].set_xlabel("Traffic Type")

    for ax in axes:
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.set_axisbelow(True)

    plt.suptitle(
        "User-Agent Analysis: Normal vs Attack Requests",
        fontsize=15,
        fontweight="bold"
    )

    plt.tight_layout()

    output_file = output_dir / "user_agent_by_attack_label.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nSaved chart: {output_file}")


def plot_encoding_impact(original_df, encoded_df):
    """Show the effect of one-hot encoding and scaling."""

    # Count original and encoded columns
    original_count = original_df.shape[1]
    encoded_count = encoded_df.shape[1]

    print("\n===== ENCODING AND SCALING IMPACT =====")
    print("Original dataset columns:", original_count)
    print("Encoded/scaled feature columns:", encoded_count)

    # Verify encoding preserves HTTP method counts
    method_columns = [
        col for col in encoded_df.columns
        if col.startswith("http_method_")
    ]

    method_counts = encoded_df[method_columns].sum()

    print("\n===== HTTP METHOD COUNTS AFTER ENCODING =====")
    print(method_counts.to_string())

    # Compare the original and encoded method frequencies
    print("\n===== ORIGINAL HTTP METHOD COUNTS =====")
    print(original_df["http_method"].value_counts())

    # Verify standard scaling
    scaled_columns = [
        "url_length",
        "response_bytes",
        "user_agent_length"
    ]

    print("\n===== SCALED FEATURE STATISTICS =====")
    print(
        encoded_df[scaled_columns]
        .agg(["mean", "std"])
        .round(3)
    )

    # Save a chart showing encoded HTTP method frequencies
    fig, ax = plt.subplots(figsize=(11, 6))

    method_counts.sort_values().plot(
        kind="barh",
        ax=ax,
        color="#702F43"
    )

    ax.set_title("HTTP Method Frequencies After One-Hot Encoding")
    ax.set_xlabel("Number of Requests")
    ax.set_ylabel("Encoded HTTP Method")

    save_chart("encoding_impact.png")


def plot_encoded_methods_vs_attacks(all_data):
    # Find all one-hot encoded HTTP method columns
    method_columns = [
        col for col in all_data.columns
        if col.startswith("http_method_")
        and col.endswith("_processed")
    ]

    # Convert attack labels to binary: 0 = normal, 1 = attack
    labels = all_data["label_attack"].fillna("").astype(str).str.strip()
    valid = ~labels.isin(["", "nan", "None"])

    data = all_data.loc[valid, method_columns].copy()
    is_attack = ~labels.loc[valid].isin(["0", "0.0"])

    # Calculate statistics for each encoded HTTP method
    summary = pd.DataFrame({
        "total_requests": data.sum(),
        "attack_requests": data.loc[is_attack].sum()
    })

    summary["attack_rate_percent"] = (
        summary["attack_requests"] /
        summary["total_requests"] * 100
    )

    # Show the number of attacks out of total requests
    summary["count_label"] = (
        summary["attack_requests"].astype(int).astype(str)
        + " / "
        + summary["total_requests"].astype(int).astype(str)
    )

    print("\n===== ATTACK COUNTS BY HTTP METHOD =====")
    print(
    summary[
        ["total_requests", "attack_requests",
         "attack_rate_percent"]
    ].round(2).to_string()
) 

    summary = summary.sort_values(
        "total_requests", ascending=False
    )

    # Save the statistics
    summary.to_csv(OUTPUT / "encoded_methods_attack_stats.csv")

    # Create chart
    fig, ax = plt.subplots(figsize=(12, 7))

    summary["attack_rate_percent"].plot(
        kind="barh",
        ax=ax,
        color="#702F43"
    )




    # Display attack count / total requests beside each bar
    for bar, label in zip(ax.patches, summary["count_label"]):
        ax.text(
        bar.get_width() + 1,
        bar.get_y() + bar.get_height() / 2,
        label,
        va="center",
        fontsize=9
    )

    ax.set_xlim(0, 120)

    ax.set_title("Encoded HTTP Methods vs Attack Labels")
    ax.set_xlabel("Attack-Labelled Requests (%)")
    ax.set_ylabel("One-Hot Encoded HTTP Method")
    ax.invert_yaxis()

    save_chart("encoded_methods_vs_attacks.png")

    print(summary.round(2).to_string())


def plot_scaling_comparison(original_df, encoded_df):
    columns = ["url_length", "response_bytes", "user_agent_length"]

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    for i, column in enumerate(columns):
        # Before scaling
        axes[0, i].hist(
        original_df[column].dropna(),
        bins=40,
        color="#376A9B"
        )
        axes[0, i].set_title(f"{column} - Before Scaling")
        axes[0, i].set_xlabel("Original Value")
        axes[0, i].set_ylabel("Requests")

        # After scaling
        axes[1, i].hist(
            encoded_df[column].dropna(),
            bins=40,
            color="#702F43"
            )
        axes[1, i].set_title(f"{column} - After Scaling")
        axes[1, i].set_xlabel("Standardised Value")
        axes[1, i].set_ylabel("Requests")

    fig.tight_layout()
    fig.savefig(
        OUTPUT / "scaling_comparison.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)

    print("Scaling comparison chart saved!")

def create_visualisations(df):
    print("\n===== CREATING VISUALISATIONS =====")

    plot_status_codes(df)
    plot_http_methods(df)
    plot_attack_labels(df)
    plot_missing_values(df)
    plot_url_lengths(df)
    plot_correlation_heatmap(df)
    plot_web_traffic_timeline(df)
    plot_status_codes_by_attack_label(df, output_dir="visuals")
    plot_attack_feature_correlations(df, output_dir="visuals")
    plot_user_agent_by_attack_label(df, output_dir="visuals")
   

    print("Charts saved in:", OUTPUT)
