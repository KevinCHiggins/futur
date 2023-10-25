from exceptions import FatalError
from question import GuessQuestion


class QuestionSetter:
    @staticmethod
    def validate_data_against_curriculum(data, curriculum):
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
        sorted_keys = sorted(curriculum.row_keys)
        sorted_rows = sorted(data.data, key=lambda row: row[key_index])
        row_keys_index = 0
        question_rows = []
        for data_row_number in range(len(sorted_rows)):
            if sorted_keys[row_keys_index] == sorted_rows[data_row_number][key_index]:
                question_rows.append(sorted_rows[data_row_number])
                row_keys_index += 1
                if row_keys_index == len(curriculum.row_keys):
                    break
        if row_keys_index != len(curriculum.row_keys):
            raise FatalError(
                "One or more primary keys specified in curriculum"
                " was not found in data.")
        return question_rows

    @staticmethod
    def _turn_rows_into_questions(selected_rows, column_names, curriculum):
        indices = [column_names.index(name) for name in curriculum.question_column_names]
        questions = []
        for row in selected_rows:
            for index in indices:
                infinitive = row[0]
                inflection_to_guess = row[index]
                inflection_name = column_names[index]
                questions.append(
                    GuessQuestion(
                        inflection_to_guess,
                        f"What is '{infinitive}' in the {inflection_name}"
                    )
                )
        return questions

    @classmethod
    def set_questions(cls, verb_data, curriculum):
        selected_rows = cls._extract_relevant_rows(verb_data, curriculum)
        return cls._turn_rows_into_questions(
            selected_rows,
            verb_data.metadata,
            curriculum
        )