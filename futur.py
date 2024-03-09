import pickle
import random
from pathlib import Path
import os
from curriculum import Curriculum
from exceptions import FatalError
from file_handling import unpickle, load_json_from_file, load_csv_from_file
from question_asker import QuestionAsker
from question_setter import QuestionSetter
from record_entry import calculate_soonest_due_date, RecordEntry
import argparse
import locale
locale.setlocale(locale.LC_COLLATE, 'fr-FR.utf-8')

from constants import (
    CURRICULA_PATH_SEGMENT,
    DATA_PATH_SEGMENT,
    DEFAULT_CURRICULUM_FILENAME,
    RECORDS_PATH_SEGMENT,
    QUESTION_WORDINGS_PATH_SEGMENT,
    PRONOUNS_FILENAME,
    RECORD_FILENAME_TEMPLATE,
    TEMPLATES_FILENAME,
    ROW_GROUPS_PATH_SEGMENT,
    ROW_GROUPS_FILENAME,
)
from verb_data import VerbData

def main(curriculum_filename=DEFAULT_CURRICULUM_FILENAME):
    pronouns_file_path = Path(QUESTION_WORDINGS_PATH_SEGMENT, PRONOUNS_FILENAME)
    pronouns = load_json_from_file(pronouns_file_path)
    question_templates_file_path = Path(QUESTION_WORDINGS_PATH_SEGMENT, TEMPLATES_FILENAME)
    question_templates = load_json_from_file(question_templates_file_path)
    row_groups_file_path = Path(ROW_GROUPS_PATH_SEGMENT, ROW_GROUPS_FILENAME)
    row_groups = load_json_from_file(row_groups_file_path)
    curriculum_file_path = Path(CURRICULA_PATH_SEGMENT, curriculum_filename)
    curriculum = Curriculum.from_dict(load_json_from_file(curriculum_file_path), row_groups)

    record_filename = RECORD_FILENAME_TEMPLATE.format(
        base=curriculum_file_path.stem,
        hash=curriculum.replicable_hash()
    )
    record_file_path = Path(RECORDS_PATH_SEGMENT, record_filename)
    if record_file_path.is_file():
        record_entries = unpickle(record_file_path)
    else:
        data_file_path = Path(DATA_PATH_SEGMENT, curriculum.data_filename)
        verb_metadata, verb_data = load_csv_from_file(data_file_path)
        verb_data = VerbData(verb_metadata, verb_data)
        question_setter = QuestionSetter(pronouns=pronouns)
        questions = question_setter.set_questions(verb_data, curriculum)
        record_entries = [
            RecordEntry(question) for question in questions
        ]

    record_entries_due = [re for re in record_entries if re.is_due()]
    random.shuffle(record_entries_due)
    question_asker = QuestionAsker(question_templates)
    for qr in record_entries_due:
        performance = question_asker.ask(qr.question)
        qr.reschedule_according_to_performance(performance)

    soonest_due_date = calculate_soonest_due_date(record_entries)
    print(f"The soonest date a question falls due is {soonest_due_date}")
    if not os.path.exists(RECORDS_PATH_SEGMENT):
        os.makedirs(RECORDS_PATH_SEGMENT)
    with open(record_file_path, "wb") as record_file:
        pickle.dump(record_entries, record_file)
        print("Wrote record for this curriculum.")


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
