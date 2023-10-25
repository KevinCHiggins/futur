from fsrs import Card, FSRS, Rating
import datetime

from constants import MAX_DATETIME

f = FSRS()


class QuestionRepetition:
    def __init__(self, question):
        self.question = question

        card = Card()
        # fix card's being initialized with datetime.datetime.utcnow()
        # in the library
        card.due = datetime.datetime.now()

        self.card = card

    def due_date(self):
        return self.card.due

    def is_due(self):
        print(f"Checking due date {self.due_date()}")
        if self.due_date() < datetime.datetime.now():
            print(f"{self.question} is due!")
            return True
        return False

    def review(self):
        rescheduled_cards = f.repeat(self.card, datetime.datetime.now())
        performance = self.question.pose()
        self.card = rescheduled_cards[performance.rating].card


def calculate_soonest_due_date(question_repetitions):
    soonest_due_date = MAX_DATETIME
    for qr in question_repetitions:
        print(qr.due_date())
        if qr.due_date() < soonest_due_date:
            soonest_due_date = qr.due_date()
    return soonest_due_date