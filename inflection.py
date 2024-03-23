SINGULAR_PERSONS = ["first person singular", "second person singular", "third person singular"]
PLURAL_PERSONS = ["first person plural", "second person plural", "third person plural"]
class Inflection:

    def __init__(self, mood, tense, person):
        self.mood = mood
        self.tense = tense
        self.person = person

    @classmethod
    def from_column_name(cls, column_name):
        return cls.from_descriptors(column_name.split("|"))

    @classmethod
    def from_descriptors(cls, parts):
        if len(parts) == 3:
            return cls(mood=parts[0], tense=parts[1], person=parts[2])
        elif len(parts) == 2:
            return cls(mood=parts[0], tense=None, person=parts[1])
        else:
            return cls(mood=parts[0], tense=None, person=None)

    @classmethod
    def all_from_column_names(cls, column_names):
        return [Inflection.from_column_name(name) for name in column_names]

    @classmethod
    def build_possible_inflections(cls, moods, tenses):
        print(moods)
        possibilities = []
        for tense in tenses:
            for mood in moods:
                for person in (SINGULAR_PERSONS + PLURAL_PERSONS):
                    print(f"Generating inflection {mood} {tense} {person}")
                    possibilities.append(cls(mood=mood, tense=tense, person=person))
        return possibilities

    def as_column_name(self):
        return f"{self.mood}|{self.tense}|{self.person}"

    def __eq__(self, other):
        return (self.mood, self.tense, self.person) == (other.mood, other.tense, other.person)

    def __hash__(self):
        return hash((self.mood, self.tense, self.person))