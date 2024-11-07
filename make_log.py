import os
import csv

from datetime import datetime

import directory_path_stuff


def write_log(log_dict,
              log_file_name=directory_path_stuff.log_file_name,
              log_file_directory=directory_path_stuff.log_file_directory):

    # convert the header and the logs to list
    log_header = list(log_dict.keys())
    log_list = list(log_dict.values())

    # get date and time
    now = datetime.now()
    now_formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    today = now.strftime("%Y-%m-%d")

    # create a list with only the date
    dated_log_header = ['Date']
    dated_log_list = [now_formatted]
    # extends the list with the elements extracted from the log list
    dated_log_header.extend(log_header)
    dated_log_list.extend(log_list)

    # build the log path with the date in the name of the file
    dated_log_file_path = f"{log_file_directory}{today}_{log_file_name}"

    # verify if the file already exists
    file_exists = os.path.exists(dated_log_file_path)

    # write the file
    with open(dated_log_file_path, 'a', newline='', encoding='utf-8') as file:
        new_log = csv.writer(file)
        if not file_exists:
            new_log.writerow(dated_log_header)
        new_log.writerow(dated_log_list)

    return True, print(f"\nLog written successfully at{dated_log_file_path}.\n")

'''
#Testing:
log_dict = { "a": "b", "c": "d"}
write_log(log_dict)
'''