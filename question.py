from enum import Enum
import datetime

from performance import Performance

QuestionType = Enum("QuestionType", ["guess"])


# will generalize later
# might also be better to generate the question text from the template
# every time rather than pickle the text
class GuessQuestion:
    def __init__(self, solution, question):
        self.solution = solution
        self.question = question

    # may get moved into a game module
    def pose(self):
        starting_time = datetime.datetime.now()
        print(self.question)
        success = (input() == self.solution)
        time_taken = datetime.datetime.now() - starting_time
        if success:
            print("Correct!")

        else:
            print("Incorrect!")
            print(f"It is: {self.solution}.")
        return Performance(time_taken, success, time_factor=(len(self.solution) / 10))

