
from conjugated_verb import ConjugatedVerb
from inflection import Inflection

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

    @classmethod
    def build_combinations(cls, verb_data, column_names, inflection_names, pronouns):
        questions = []
        selected_inflections = [Inflection.from_column_name(name) for name in inflection_names]
        infinitive = Inflection.from_column_name("infinitive")

        inflections = Inflection.all_from_column_names(column_names) # needed till ConjugatedVerb becomes a service
        verb = ConjugatedVerb.from_row_and_inflection_descriptions(verb_data, inflections)
        infinitive_of_verb = verb[infinitive]

        for selected_inflection in selected_inflections:
            questions.append(
                cls(
                    solution=verb[selected_inflection],
                    infinitive=infinitive_of_verb,
                    tense=selected_inflection.tense,
                    french_pronoun=pronouns[selected_inflection.person]["French"],
                )
            )
        return questions

class DistinguishTenseQuestion:
    def __init__(self, solution, inflected_verb, possible_tenses, french_pronoun):
        self.solution = solution
        self.inflected_verb = inflected_ver
        self.possible_tenses = possible_tenses
        self.french_pronoun = french_pronoun

    def generate_text(self, template):
        return template.format(
            solution=self.solution,
            inflected_verb=self.inflected_verb,
            possible_tenses=self.possible_tenses,
            french_pronoun=self.french_pronoun,
        )
