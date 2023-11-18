from exceptions import FatalError
from constants import QuestionType

from hashlib import sha256


class Curriculum:
    def replicable_hash(self):
        rep_hash = sha256()
        for bytes_obj in self._properties_as_bytes_objects():
            rep_hash.update(bytes_obj)
        return rep_hash.hexdigest()

    @staticmethod
    def _as_bytes_obj(val):
        if isinstance(val, QuestionType):
            val = val.name
        if isinstance(val, list):
            val = ",".join(val)
        return bytes(val, "utf-8")

    def _properties_as_bytes_objects(self):
        return [self._as_bytes_obj(self.__dict__[attr]) for attr in vars(self)]

    def __init__(
            self,
            data_filename,
            question_type,
            question_column_names,
            row_keys,
            key_column_name
    ):
        self.data_filename = data_filename
        self.question_type = question_type
        self.question_column_names = question_column_names
        self.row_keys = row_keys
        self.key_column_name = key_column_name

    @classmethod
    def _require_non_empty_list(cls, attributes, key):
        value = attributes[key]
        if not isinstance(value, list):
            raise FatalError(
                f"List of {key} not found in curriculum.")
        if len(value) == 0:
            raise FatalError(f"There must be at least one element in the list of {key}"
                             " found in curriculum.")
        return value

    @classmethod
    def from_dict(cls, attributes):
        try:
            data_filename = (attributes["data"])
            type_text = attributes["type"]
            question_column_names = cls._require_non_empty_list(
                attributes,
                "column names"
            )
            row_keys = cls._require_non_empty_list(
                attributes,
                "row keys"
            )
            key_column_name = attributes["key column name"]
        except KeyError as e:
            raise FatalError(
                f"Curriculum is missing expected '{e.args[0]}' attribute.")
        try:
            question_type = QuestionType[type_text]
        except KeyError as e:
            raise FatalError(
                f"'{e.args[0]}' is not a recognised question type."
            )
        return cls(
            data_filename,
            question_type,
            question_column_names,
            row_keys,
            key_column_name)
