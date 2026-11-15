
import csv

# Combines each Apache access log entry with its two corresponding attack labels
def merge_files(access_filename, label_filename, output_filename):

    # Read access file in read mode
    with open(access_filename, "r") as file:
          access_log = file.readlines()

    #Read label file in read mode
    with open(label_filename, "r") as file:
        label_log = file.readlines()


    # Create output file with merged output
    with open(output_filename, "w", newline="") as file:
        #creates a csv writer called output. This writes data into the output file as formatted CSV rows
        output = csv.writer(file)

        #Create Header for output file

        output.writerow(["line_no", "access_data", "label_time", "label_attack"]) 

        # Merge each Line

        for i in range(len(label_log)):
            #increment line nunmber
            line_number = i + 1
            log_line = access_log[i]
            label_line = label_log[i]
            # First strip removes whitespace and second split with , separates the two labels at the comma
            labels = label_line.strip().split(",")

            output.writerow([
                line_number,    # Contains the line number
                log_line.rstrip("\r\n"),  # Contains the Apache access record with its line ending characters
                labels[0].strip(),   # Saves the first label
                labels[1].strip()    # Saves the second label
            ])



#Categorises the Apache log entry into separate columns
def parse_merged_file(input_filename, output_filename):


    successful = 0   #counts records parsed without an error
    failed = 0       #counts records that could be not be parsed

    with open(input_filename, "r", encoding="utf-8", newline="") as input_file, \
         open(output_filename, "w", encoding="utf-8", newline="") as output_file:

        #Prepares CSV file so each record can be read. It does not load the entire CSV file into memory immediately
        reader = csv.DictReader(input_file)
        writer = csv.writer(output_file)

        #Create Header columns
        writer.writerow([
            "line_no",
            "ip_address",
            "identity",             # Client Identity
            "username",             # Authenticated USer 
            "timestamp",
            "http_method",          # Type of http request such as GET, POST etc
            "url_path",             # Web page or resource begin requested
            "http_version",
            "status_code",          # The server's HTTP response e.g. 200 - success, 404 - not found, 500 - server error
            "response_bytes",       # Size of the HTTP response body
            "referrer",             # The web page the client reports visiting before making the request
            "user_agent",           # Info supplied by client about its browser, OS
            "parse_error",          # Records if there is a parser error
            "access_data",          # Original Apache access log
            "label_time",           # Contains an attack name or 0
            "label_attack"          # Contains an attack name or 0. This is chosen classification target
        ])

        for row in reader:

            #Retrieves the original Apache log entry
            log = row["access_data"]

            try:
                # Extract the final quoted user agent
                before_user_agent, user_agent, end = log.rsplit('"', 2)
                #Checks for unexpected text after the user agent
                if end.strip():
                    raise ValueError("There is unexpected text after user agent")

                # Extract the quoted referrer
                before_referrer, referrer, separator = before_user_agent.rsplit('"', 2)

                if separator.strip():
                    raise ValueError("Invalid referrer separator")

                # Extract the beginning and HTTP request
                beginning_text, request_and_response = before_referrer.split('"', 1)
                request_text, response_text = request_and_response.rsplit('"', 1)

                # Parse IP address and timestamp
                beginning = beginning_text.strip().split()

                if len(beginning) != 5:
                    raise ValueError("Invalid beginning")

                ip_address = beginning[0]
                identity = beginning[1]
                username = beginning[2]

                # Reconstructs the timestamp and timezone taking out the square brackets
                # Format is 04/Mar/2020:18:34:12 +0000
                timestamp = (
                    beginning[3].strip("[")
                    + " "
                    + beginning[4].strip("]")
                )

                # Parse HTTP request
                request = request_text.split()

                if len(request) != 3:
                    raise ValueError("Invalid HTTP request")

                http_method = request[0]
                url_path = request[1]
                http_version = request[2]

                # Parse HTTP response
                response = response_text.strip().split()

                if len(response) != 2:
                    raise ValueError("Invalid response")

                status_code = response[0]
                response_bytes = response[1]

                parsed_fields = [
                    ip_address,
                    identity,
                    username,
                    timestamp,
                    http_method,
                    url_path,
                    http_version,
                    status_code,
                    response_bytes,
                    referrer,
                    user_agent
                ]

                parse_error = ""
                successful += 1

            except (ValueError, IndexError) as error:

                parsed_fields = [""] * 11
                parse_error = str(error)
                failed += 1

                print("Failed line:", row["line_no"])
                print("Reason:", parse_error)
                print("Original log:", log)
                print()

            #Writes the parsed record, original log and two labels into the CSV
            writer.writerow([
                row["line_no"],
                *parsed_fields,  # The * unpacks the list into 11 fields. Take all 11 values and insert them indiviually
                parse_error,
                log,
                row["label_time"],
                row["label_attack"]
            ])

    print("\nSuccessfully parsed:", successful)
    print("Failed to parse:", failed)
    print("Total rows:", successful + failed)

    return failed == 0
