from csv import Error as CSVError
from csv import reader as csv_reader
from exceptions import FatalError


class VerbData:
    def __init__(self, metadata, data):
        self.metadata = metadata
        self.data = data

    @classmethod
    def from_csv(cls, raw_csv):
        try:
            parsed_csv = [row for row in csv_reader(raw_csv)]
        except CSVError:
            raise FatalError(f"Error parsing CSV data.")

        if len(parsed_csv) == 0:
            raise FatalError(f"No data found in CSV file.")
        return cls(parsed_csv[0], parsed_csv[1:])
