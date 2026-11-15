
import csv
from collections import Counter


def check_data_quality(filename):

    total_rows = 0
    missing_values = Counter()
    status_codes = Counter()
    http_methods = Counter()
    time_labels = Counter()
    attack_labels = Counter()
    parsing_errors = 0

    with open(filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_rows += 1

            # Count missing values
            for column, value in row.items():
                if value is None or value.strip() == "":
                    missing_values[column] += 1

            # Count HTTP status codes
            status_codes[row["status_code"]] += 1

            # Count HTTP methods
            http_methods[row["http_method"]] += 1

            # Count both original labels
            time_labels[row["label_time"]] += 1
            attack_labels[row["label_attack"]] += 1

            # Count parsing errors
            if row["parse_error"]:
                parsing_errors += 1

    print("\n===== DATA QUALITY REPORT =====")

    print("\nTotal rows:", total_rows)
    print("Parsing errors:", parsing_errors)

    print("\nMissing values:")
    for column, count in missing_values.items():
        print(column, ":", count)

    print("\nHTTP methods:")
    for method, count in http_methods.items():
        print(method, ":", count)

    print("\nHTTP status codes:")
    for status, count in status_codes.items():
        print(status, ":", count)

    print("\nTime labels:")
    for label, count in time_labels.items():
        print(repr(label), ":", count)

    print("\nAttack labels:")
    for label, count in attack_labels.items():
        print(repr(label), ":", count)
