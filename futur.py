import datetime
import pickle
import random
from pathlib import Path

from curriculum import Curriculum
from exceptions import FatalError
from file_handling import read, read_lines, unpickle, load_json_from_file, load_csv_from_file
from question_setter import QuestionSetter
from question_repetition import QuestionRepetition, calculate_soonest_due_date
import argparse

from constants import (
    CURRICULA_PATH_SEGMENT,
    DATA_PATH_SEGMENT,
    DEFAULT_CURRICULUM_FILENAME,
    RECORDS_PATH_SEGMENT,
    QUESTION_WORDINGS_PATH_SEGMENT,
    COLUMN_RENAMINGS_FILENAME,
    TEMPLATE_FILENAME, RECORD_FILENAME_TEMPLATE
)
from verb_data import VerbData


def main(curriculum_filename=DEFAULT_CURRICULUM_FILENAME):
    column_renamings_file_path = Path(QUESTION_WORDINGS_PATH_SEGMENT, COLUMN_RENAMINGS_FILENAME)
    renamings = load_json_from_file(column_renamings_file_path)
    question_template_file_path = Path(QUESTION_WORDINGS_PATH_SEGMENT, TEMPLATE_FILENAME)
    question_template = read(question_template_file_path)
    curriculum_file_path = Path(CURRICULA_PATH_SEGMENT, curriculum_filename)
    curriculum = Curriculum.from_dict(load_json_from_file(curriculum_file_path))

    record_filename = RECORD_FILENAME_TEMPLATE.format(
        base=curriculum_file_path.stem,
        hash=curriculum.replicable_hash()
    )
    record_file_path = Path(RECORDS_PATH_SEGMENT, record_filename)
    if record_file_path.is_file():
        question_repetitions = unpickle(record_file_path)
    else:
        data_file_path = Path(DATA_PATH_SEGMENT, curriculum.data_filename)
        verb_metadata, verb_data = load_csv_from_file(data_file_path)
        verb_data = VerbData(verb_metadata, verb_data)
        question_setter = QuestionSetter(renamings=renamings, template=question_template)
        question_setter.validate_data_against_curriculum(verb_data, curriculum)
        questions = question_setter.set_questions(verb_data, curriculum)
        question_repetitions = [QuestionRepetition(question) for question in questions]

    question_repetitions_due = [qr for qr in question_repetitions if qr.is_due()]
    random.shuffle(question_repetitions_due)
    for qr in question_repetitions_due:
        qr.review()

    soonest_due_date = calculate_soonest_due_date(question_repetitions)
    print(f"The soonest date a question falls due is {soonest_due_date}")
    with open(record_file_path, "wb") as record_file:
        pickle.dump(question_repetitions, record_file)
        print("Wrote record of question repetitions for this curriculum.")


parser = argparse.ArgumentParser(
    prog="python3 futur.py",
    description="Spaced repetition verb endings quiz",
    epilog="You just read the help text."
)
parser.add_argument(
    "curriculum_filename",
    nargs="?",
    default=DEFAULT_CURRICULUM_FILENAME,
    help=f"Enter the filename (no path) of a curriculum file present in {CURRICULA_PATH_SEGMENT}"
)
args = parser.parse_args()

try:
    main(curriculum_filename=args.curriculum_filename)
except FatalError as fe:
    print(str(fe))
    exit(1)
