import csv
import os

def get_csv_folder():
    csv_path = './CSV'
    if not os.path.isdir(csv_path):
        os.makedirs(csv_path)
    return csv_path + '/'

def check_file_exists(filename):
    return True if os.path.isfile(filename) else False

def write_to_csv(filename, fieldnames=[], rows=[]):
    csv_path = get_csv_folder()

    mode = 'w'
    file_path = csv_path + filename
    if check_file_exists(file_path):
        mode = 'a'

    with open(csv_path + filename, mode, newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if mode == 'w':
            writer.writeheader()
        for row in rows:
            writer.writerow(row)
        csvfile.close()


def write_details_to_csv(filename, details):
    try:
        if details:
            # get csv file headers
            header = [key for key in details[0].keys()]
            print(header)
            # Write to csv file
            write_to_csv(filename, header, details)
    except Exception as e:
        print('*************** Error while write to csv *************')
        print(e)
        pass