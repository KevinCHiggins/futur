from datetime import timedelta
from fsrs import Rating
from constants import BASE_TIME


class Performance:
    def __init__(self, time_taken, success, time_factor):
        self.time_taken = time_taken
        if not success:
            self.rating = Rating.Again
            print("Again")
        else:
            if time_taken < timedelta(seconds=BASE_TIME) * time_factor:
                self.rating = Rating.Easy

                print("Easy")
            elif time_taken < timedelta(seconds=BASE_TIME * 2) * time_factor:
                self.rating = Rating.Good

                print("Good")
            else:
                self.rating = Rating.Hard

                print("Hard")
