from inflection import Inflection
from constants import QuestionType
from exceptions import FatalError

class QuestionService:
    def __init__(self, conjugated_verb_service):
        self.conjugated_verb_service = conjugated_verb_service


# remove column_names
    def build_combinations(self, question_type, verb_data, moods, tenses, pronouns):
        questions = []


        verb = self.conjugated_verb_service.from_row(verb_data)

        if question_type == QuestionType.guess:
            selected_inflections = Inflection.build_possible_inflections(moods=moods, tenses=tenses)
            infinitive = Inflection.from_column_name("infinitive")
            infinitive_of_verb = verb[infinitive]
            for selected_inflection in selected_inflections:
                questions.append(
                    GuessQuestion(
                        solution=verb[selected_inflection],
                        infinitive=infinitive_of_verb,
                        tense=selected_inflection.tense,
                        french_pronoun=pronouns[selected_inflection.person]["French"],
                    )
                )
        elif question_type == QuestionType.distinguish_tense:
            # for now let's assume
            if len(tenses) != 2:
                raise FatalError("DistinguishTenseQuestion takes strictly two tenses and one mood for now.")
            tense_1_inflections = Inflection.build_possible_inflections(moods=[moods[0]], tenses=[tenses[0]])
            tense_2_inflections = Inflection.build_possible_inflections(moods=[moods[0]], tenses=[tenses[1]])
            pairs = zip(tense_1_inflections, tense_2_inflections)
            for pair in pairs:
                questions.append(
                    DistinguishTenseQuestion(
                        solution=tenses[0],
                        inflected_verb=verb[pair[0]],
                        possible_tenses=tenses,
                        french_pronoun=pronouns[pair[0].person]["French"],
                    )
                )
                questions.append(
                    DistinguishTenseQuestion(
                        solution=tenses[1],
                        inflected_verb=verb[pair[1]],
                        possible_tenses=tenses,
                        french_pronoun=pronouns[pair[0].person]["French"], # person is the same per pair
                    )
                )


        return questions

class GuessQuestion:
    def __init__(self, solution, infinitive, tense, french_pronoun):
        self.solution = solution
        self.infinitive = infinitive
        self.tense = tense
        self.french_pronoun = french_pronoun

    def generate_text(self, template):
        return template.format(
            infinitive=self.infinitive,
            tense=self.tense,
            french_pronoun=self.french_pronoun,
        )



class DistinguishTenseQuestion:
    def __init__(self, solution, inflected_verb, possible_tenses, french_pronoun):
        self.solution = solution
        self.inflected_verb = inflected_verb
        self.possible_tenses = possible_tenses
        self.french_pronoun = french_pronoun

    def generate_text(self, template):
        return template.format(
            solution=self.solution,
            inflected_verb=self.inflected_verb,
            possible_tenses=self.possible_tenses,
            french_pronoun=self.french_pronoun,
        )
