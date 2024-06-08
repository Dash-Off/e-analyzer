from gramformer import Gramformer

class GrammarChecker:
  '''
  VERB (20): Verb errors are critical because they often affect the sentence structure and meaning.
  NOUN (15): Noun errors can significantly alter the meaning of a sentence.
  ADP (10): Preposition errors are common and important for sentence clarity.
  DET (10): Determiner errors are frequent and affect the specificity and definiteness of nouns.
  PRON (8): Pronoun errors impact the clarity and coherence of references.
  ADV (7): Adverb errors affect the description of actions and events.
  ADJ (7): Adjective errors affect the description of nouns.
  PUNCT (5): Punctuation errors can drastically change the meaning and readability of sentences.
  SPELL (5): Spelling errors, while often minor, can impact readability and professionalism.
  WO (4): Word order errors affect the sentence's syntactic structure and clarity.
  CONJ (3): Conjunction errors impact the logical flow of sentences.
  NUM (2): Numeral errors, while less frequent, can affect the accuracy of information.
  MORPH (2): Morphological errors impact the structure of words.
  ORTH (1): Orthographic errors are typically minor but can affect readability.
  PRT (1): Particle errors are less common and usually have a minor impact.
  OTHER (0): Other types are varied and less predictable, often less impactful overall.
  '''
  SCORES = {
    "VERB": 20,
    "NOUN": 15,
    "ADP": 10,
    "DET": 10,
    "PRON": 8,
    "ADV": 7,
    "ADJ": 7,
    "PUNCT": 5,
    "SPELL": 5,
    "WO": 4,
    "CONJ": 3,
    "NUM": 2,
    "MORPH": 2,
    "ORTH": 1,
    "PREP": 1,
    "OTHER": 0
  }

  def __init__(self) -> None:
    self.model = Gramformer(models=1, use_gpu=False)
  
  def __pre_process(self, sentence):
    self.sentence = sentence
    self.edits = []
    for corrections in self.model.correct(self.sentence, 2):
      for edit in self.model.get_edits(self.sentence, corrections):
        self.edits.append(edit)

  
  def __get_score(self) -> int:
    score = 0
    for edit in edit:
      score += self.SCORES[edit[0]]
    return score

  def __normalize_scores(self, scores: list):
    return sum(scores) / (sum(self.SCORES.values()) * len(scores))

  def process(self, sentences):
    '''Process sentences to find errors and provide the total scoring of the sentences'''
    scores = []
    for sentence in sentences:
      self.__pre_process(sentence=sentence)
      scores.append(self.__get_score())
    return self.__normalize_scores(scores)

  
