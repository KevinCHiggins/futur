from datetime import datetime
from performance import Performance

class QuestionAsker:
    def __init__(self, templates):
        self.templates = templates

    def ask(self, question, prefix):
        question_cls = question.__class__.__name__
        question_text = prefix + question.generate_text(self.templates[question_cls])
        starting_time = datetime.now()
        print(question_text)
        success = (input() == question.solution)
        time_taken = datetime.now() - starting_time
        if success:
            print("Correct!")

        else:
            print("Incorrect!")
            print(f"It is: {question.solution}.")
        return Performance(time_taken, success, time_factor=(len(question.solution) / 10))
