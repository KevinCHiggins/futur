from exceptions import FatalError

class ConjugatedVerb:
    @classmethod
    def from_row_and_inflection_descriptions(cls, row, inflection_descriptions):
        if len(row) != len(inflection_descriptions):
            print(row)
            print(inflection_descriptions)
            raise FatalError("Number of inflection descriptions does not match number of inflections")
        result = {}

        for i in range(len(row)):
            result[inflection_descriptions[i]] = row[i]
        return result
