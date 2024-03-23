import datetime
from enum import Enum

QuestionType = Enum("QuestionType", ["guess", "distinguish_tense"])
CURRICULA_PATH_SEGMENT = "./curricula"
DATA_PATH_SEGMENT = "./data"
DEFAULT_CURRICULUM_FILENAME = "dist-future-conditional-avoir.json"
RECORDS_PATH_SEGMENT = "./records"
RECORD_FILENAME_TEMPLATE = "{base}-{hash}.pickle"
QUESTION_WORDINGS_PATH_SEGMENT = "./question-wordings"
PRONOUNS_FILENAME = "pronouns.json"
ROW_GROUPS_PATH_SEGMENT = "./verb-groups"
ROW_GROUPS_FILENAME = "verb-groups.json"
TEMPLATES_FILENAME = "templates.json"
BASE_TIME = 2.0  # max time taken to type a 10-char answer that is still considered better than a Good rating
MAX_DATETIME = datetime.datetime(datetime.MAXYEAR, 1, 1, 0, 0, 0)