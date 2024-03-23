from exceptions import FatalError

class ConjugatedVerbService:
    def __init__(self, inflection_descriptions):
        self.inflection_descriptions = inflection_descriptions


    def from_row(self, row):
        if len(row) != len(self.inflection_descriptions):
            print(row)
            print(inflection_descriptions)
            raise FatalError("Number of inflection descriptions does not match number of inflections")
        result = {}

        for i in range(len(row)):
            result[self.inflection_descriptions[i]] = row[i]
        return result
