import csv
from zipfile import ZipFile
import os.path
from os import path


def read_file(file, header=True):
    """#Logic to read the new file"""
    print('processing file: ', file)

    result = {}

    with open(file, "r") as f:
        try:
            reader = csv.reader(f, delimiter=",")
            env = ((f.name).split('\\')[-1]).split('.')[0]
            env = ''.join([i for i in env if not i.isdigit()])
            print('env: ', env)
            if header:
                next(reader)
            for row in reader:
                if row:
                    result[str(row[0])] = env
        finally:
            f.close()
    return result


def insert_data(file, data):
    with open(file[0], mode='a', newline='') as f:
        writer = csv.writer(f)
        for key, value in data.items():
            print('inserting ', key, ' --> ', value)
            writer.writerow([key, value])
    f.close()


def extract_zip_file(directory, file_name):
    file_name = directory + "\\" + file_name
    with ZipFile(file_name, 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()
        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall()
        print('Done!')


def check_file(path, file_name):
    result = []
    for root, dirs, files in os.walk(path):
        if file_name in files:
            result.append(os.path.join(root, file_name))
    print('result:', result)
    return result


def get_all_csv(path, combined_file):
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                result.append(os.path.join(root, file))
    result = [s for s in result if str(combined_file) not in s]

    return result


def process_file(file, combined_data, combined_file):
    print("passing file: ", file)
    result_new = read_file(file)
    print('source_ip_new: ', result_new.keys())
    print('env_new: ', result_new.values())

    updated_result = {}
    for key, value in result_new.items():
        if key not in combined_data.keys():
            print(key, ' NOT In ', combined_data.keys(), ' -----> value: ', value)
            updated_result[key] = value
        else:
            print(key, ' FOUND in ', combined_data.keys())
    del result_new
    print('updated source_ip_new: ', updated_result.keys())
    print('updated env: ', updated_result.values())

    if updated_result:
        insert_data(combined_file, updated_result)


def main():

    directory = 'c:\\My Docs\\TCS'
    file_name = 'Engineering Test.zip'
    current_path = os.path.dirname(os.path.realpath(__file__)) + '\\' + file_name.split(".")[0]
    combined_file = 'Combined.csv'

    extract_zip_file(directory, file_name)
    combined_file = check_file(current_path, combined_file)
    if combined_file:
        print(combined_file, ' exists')
    else:
        print(combined_file, ' does not exist')

    combined_data = read_file(combined_file[0])
    print('source_ip: ', combined_data.keys())
    print('env: ', combined_data.values())

    print('current_path: ', current_path)
    csv_list = get_all_csv(current_path, combined_file)
    print('csv_list: ', csv_list)
    for file in csv_list:
        if file != combined_file:
            process_file(file, combined_data, combined_file)
        else:
            print('Not passing ==========>', combined_file)


if __name__ == "__main__":
    main()
