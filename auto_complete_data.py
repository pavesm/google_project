class AutoCompleteData:
    def __init__(self, completed_sentence, source_text, offset, score):
        self.completed_sentence = completed_sentence
        self.source_text = source_text
        self.offset = offset
        self.score = score
