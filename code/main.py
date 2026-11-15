# Import Functions from Files
# COM774 File Handling functionality
from initial_checks import check_row_counts   # Initial Checks on Files
from file_handling import (merge_files, parse_merged_file)
from check_parsed_data import check_data_quality
from data_cleansing import prepare_data
from transform_data import transform_data
from pathlib import Path
from data_encode import encoding_scaling
import pandas as pd
from visualise_data import (
    create_visualisations,
    plot_encoding_impact,
    plot_encoded_methods_vs_attacks,
    plot_scaling_comparison
)
import os

os.chdir(Path(__file__).resolve().parent)


#Check Files count for mail.cup.com-access data access logs against mail.cup.com-access labelling file
line_count_match = check_row_counts(
     r"C:\COM774_CW1_MT\code\data\mail.cup.com-access.log",
    r"C:\COM774_CW1_MT\label\mail.cup.com-access.log"
)

# Ensure Apache logs and labelled access logs have the same number of lines
if not line_count_match:
    raise ValueError(
        "Processing stopped. File count does not match"
    )

print("Result:", line_count_match)



if line_count_match:
    merge_files("data/mail.cup.com-access.log",   #Apache access log file
                "label/mail.cup.com-access.log",  #Apache label file containing 2 fields
                "merge_mail.cup.com.log")         #Output of Merged file

#Parse merged file created from above and output to parsed_output_mail.cup.csv
parse_merged_file("merge_mail.cup.com.log", "parsed_output_mail.cup.csv")

print ("========Call Check Data Quality============")
check_data_quality("parsed_output_mail.cup.csv")

prepared_df=prepare_data("parsed_output_mail.cup.csv")

print ("========Transform Data============")
transformed_df=transform_data(prepared_df)

encode_df = encoding_scaling(transformed_df)
print(encode_df.head().to_string(index=False))
all_data = pd.concat(
    [transformed_df, encode_df.add_suffix("_processed")],
    axis=1
)

Path("encoding_results").mkdir(exist_ok=True)

all_data.to_csv(
    "encoding_results/all_preprocessed_data.csv",
    index=False
)

# Original categorical features
print("\n===== BEFORE ENCODING =====")
print(
    transformed_df[
        ["http_method", "status_code"]
    ].head(10).to_string(index=False)
)

# Encoded categorical features
encoded_columns = [
    col for col in encode_df.columns
    if col.startswith(("http_method_", "status_code_"))
]




print("\n===== AFTER ENCODING =====")
print(
    encode_df[encoded_columns]
    .head(10)
    .to_string(index=False)
)

# Measure the impact
print("\n===== IMPACT OF ENCODING =====")
print("Original categorical columns:", 2)
print("Encoded categorical columns:", len(encoded_columns))
print("New columns created:", len(encoded_columns) - 2)

transformed_df.to_csv(
    Path("transformed") / "mail_cup_processed.csv",
    index=False
)

print(prepared_df.head(10))

# Display the returned DataFrame
print("\n===== TRANSFORMED DATAFRAME =====")
print("\n===== COLUMN HEADERS =====")
print(transformed_df.columns.tolist())

print("\n===== FIRST 5 ROWS =====")
print(transformed_df.head().to_string(index=False))

print(type(transformed_df))
print(transformed_df.shape)

# Generate charts
create_visualisations(transformed_df)

plot_encoding_impact(transformed_df, encode_df)
plot_scaling_comparison(transformed_df, encode_df)

plot_encoded_methods_vs_attacks(all_data)


print(transformed_df.columns.tolist())
print("Number of columns:", len(transformed_df.columns))
print("\nPreparation completed successfully!")

