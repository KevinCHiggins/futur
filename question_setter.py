from exceptions import FatalError
from question import GuessQuestion
import locale


class QuestionSetter:
    def __init__(self, renamings, templates):
        self.renamings = renamings
        self.templates = templates

    @staticmethod
    def _validate_data_against_curriculum(data, curriculum):
        required_column_names = curriculum.question_column_names + [curriculum.key_column_name]
        all_column_names = data.metadata
        for column_name in required_column_names:
            if column_name not in all_column_names:
                raise FatalError(
                    f"Column name {column_name} specified in curriculum"
                    " not found in data.")

    @staticmethod
    def _extract_relevant_rows(data, curriculum):
        all_column_names = data.metadata
        key_index = all_column_names.index(curriculum.key_column_name)
        # can't think of any need to maintain user's original order
        sorted_keys = sorted(curriculum.row_keys, key = locale.strxfrm)
        sorted_rows = sorted(data.data, key=lambda row: locale.strxfrm(row[key_index]))
        row_keys_index = 0
        question_rows = []
        print(sorted_keys)
        for data_row_number in range(len(sorted_rows)):
            if sorted_keys[row_keys_index] == sorted_rows[data_row_number][key_index]:
                question_rows.append(sorted_rows[data_row_number])
                row_keys_index += 1
                if row_keys_index == len(curriculum.row_keys):
                    break
        if row_keys_index != len(curriculum.row_keys):
            print(f"row keys index {row_keys_index} {len(curriculum.row_keys)} {len(sorted_rows)}")
            raise FatalError(
                "One or more primary keys specified in curriculum"
                " was not found in data.")
        return question_rows

    def _turn_rows_into_questions(self, selected_rows, column_names, curriculum):
        indices = [column_names.index(name) for name in curriculum.question_column_names]
        questions = []
        for row in selected_rows:
            for index in indices:
                infinitive = row[0]
                inflection_to_guess = row[index]
                inflection_name = self.renamings[column_names[index]]
                questions.append(
                    GuessQuestion(
                        solution=inflection_to_guess,
                        infinitive=infinitive,
                        inflection_name=inflection_name,
                    )
                )
        return questions

    def set_questions(self, verb_data, curriculum):
        self._validate_data_against_curriculum(verb_data, curriculum)
        selected_rows = self._extract_relevant_rows(verb_data, curriculum)
        return self._turn_rows_into_questions(
            selected_rows,
            verb_data.metadata,
            curriculum
        )