import os   #Enabled to change directory

def count_file_lines(filename):

    os.chdir(r"C:\COM774_CW1_MT")
    print(os.getcwd())
    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        return sum(1 for line in file)



def check_row_counts(log_filename, label_filename):

    log_access_rows = count_file_lines(log_filename)
    label_access_rows = count_file_lines(label_filename)

    print("Apache Access lines:", log_access_rows)
    print("Apache Label lines:", label_access_rows)

    if log_access_rows == label_access_rows:
        print("Apache access log and label access files have identical numbe of lines")
        return True
    else:
        print("Files do not have equal number of lines")
        return False



