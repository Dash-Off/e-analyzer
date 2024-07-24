import textstat
from nltk.tokenize import word_tokenize


SAFE_LIMIT_DIVERSITY = 65 # In percentage, anything diverse than 65 is too diverse in topic

class VocabularyAnalyzer:
  def get_ease_score(self, text):
    flesh_score = textstat.flesch_reading_ease(text)
    eflaw_score = 100 - textstat.mcalpine_eflaw(text) # Eflaw score less => more easy to read

    return sum([flesh_score, eflaw_score]) / 2

  def get_lexical_diversity(self, text):
    tokens = word_tokenize(text)
    unique_tokens = set(tokens)
    diversity = len(unique_tokens) / len(tokens)
    return diversity * 100

  def get_score(self,text):
    diverse = self.get_lexical_diversity(text=text)
    easeness = self.get_ease_score(text=text)
    
    diversity = 100 - abs(35 - diverse) # 35 => 100% or ideal diverse
    return sum([easeness, diversity])/2

  def process(self, sentences):
    text = ""
    self.easeness_scores = {}
    for index, sentence in enumerate(sentences):
      text += sentence
      score = self.get_ease_score(sentence)
      if score < 50:
        self.easeness_scores[(index, sentence)] = self.get_ease_score(sentence)

    return self.get_score(text)

    