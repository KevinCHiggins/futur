import pickle
from csv import Error as CSVError
from csv import reader as csv_reader

from exceptions import FatalError
from json import JSONDecodeError
from json import loads as json_load_string


def read(path):
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError as e:
        raise FatalError(f"File {path} not found.")


def read_lines(path):
    try:
        with open(path, "r") as file:
            return file.readlines()
    except FileNotFoundError as e:
        raise FatalError(f"File {path} not found.")


def unpickle(path):
    try:
        with open(path, "rb") as record_file:
            return pickle.load(record_file)
    except FileNotFoundError as e:
        raise FatalError(f"File {path} not found.")


def load_csv_from_file(path):
    lines = read_lines(path)
    try:
        parsed_csv = [row for row in csv_reader(lines)]
    except CSVError:
        raise FatalError(f"Error parsing CSV data.")

    if len(parsed_csv) == 0:
        raise FatalError(f"No data found in CSV file.")
    return parsed_csv[0], parsed_csv[1:]


def load_json_from_file(path):
    try:
        return json_load_string(read(path))
    except JSONDecodeError as e:
        raise FatalError(f"Could not parse JSON.")