import datetime
import pickle
import random
from pathlib import Path

from curriculum import Curriculum
from exceptions import FatalError
from question_setter import QuestionSetter
from question_repetition import QuestionRepetition, calculate_soonest_due_date

from constants import (
    CURRICULA_PATH_SEGMENT,
    DATA_PATH_SEGMENT,
    DEFAULT_CURRICULUM_FILENAME,
    RECORDS_PATH_SEGMENT, MAX_DATETIME
)
from verb_data import VerbData


def main(curriculum_filename = DEFAULT_CURRICULUM_FILENAME):
    curriculum_file_path = Path(
        CURRICULA_PATH_SEGMENT,
        curriculum_filename
    )
    try:
        with open(curriculum_file_path, "r") as curriculum_file:
            curriculum_json = curriculum_file.read()
            curriculum = Curriculum.from_json(curriculum_json)
    except FileNotFoundError as e:
        raise FatalError(f"Curriculum file {curriculum_file_path} not found.")
    data_file_path = Path(DATA_PATH_SEGMENT, curriculum.data_filename)
    try:
        with open(data_file_path, "r", newline="") as data_file:
            verb_data_csv_lines = data_file.readlines()  # TODO harmonise w/ CSV
    except FileNotFoundError:
        raise FatalError(f"Data file {data_file_path} specified in"
                         f" {curriculum_file_path} does not exist.")
    record_filename = f"{curriculum_file_path.stem}-{curriculum.replicable_hash()}.pickle"
    record_file_path = Path(RECORDS_PATH_SEGMENT, record_filename)
    if record_file_path.is_file():
        with open(record_file_path, "rb") as record_file:
            question_repetitions = pickle.load(record_file)
            print("Read record of question repetitions for this curriculum.")
            print(f"Amount of questions: {len(question_repetitions)}")
    else:
        print("No record found for repetitions of this curriculum's questions.\n"
              "Generating afresh...")
        verb_data = VerbData.from_csv(verb_data_csv_lines)
        QuestionSetter.validate_data_against_curriculum(verb_data, curriculum)
        questions = QuestionSetter.set_questions(verb_data, curriculum)
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


try:
    main()
except FatalError as fe:
    print(str(fe))
    exit(1)
