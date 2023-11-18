import datetime
from enum import Enum

QuestionType = Enum("QuestionType", ["guess"])
CURRICULA_PATH_SEGMENT = "./curricula"
DATA_PATH_SEGMENT = "./data"
DEFAULT_CURRICULUM_FILENAME = "future-irregular-manger.json"
RECORDS_PATH_SEGMENT = "./records"
RECORD_FILENAME_TEMPLATE = "{base}-{hash}.pickle"
QUESTION_WORDINGS_PATH_SEGMENT = "./question-wordings"
COLUMN_RENAMINGS_FILENAME = "column-renamings.json"
TEMPLATES_FILENAME = "templates.json"
BASE_TIME = 2.0  # max time taken to type a 10-char answer that is still considered better than a Good rating
MAX_DATETIME = datetime.datetime(datetime.MAXYEAR, 1, 1, 0, 0, 0)