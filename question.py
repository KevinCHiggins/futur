class GuessQuestion:
    def __init__(self, solution, infinitive, inflection_name):
        self.solution = solution
        self.infinitive = infinitive
        self.inflection_name = inflection_name

    def generate_text(self, template):
        return template.format(
                            infinitive=self.infinitive,
                            inflection_name=self.inflection_name
                        )
