from eanalyze.vocabulary_analyzer import VocabularyAnalyzer
from eanalyze.text_processor import TextProcessor
from eanalyze.relevance_analyzer import RelevanceAnalyzer
from eanalyze.grammar_checker import GrammarChecker
from threading import Thread

'''
20Relevence < 35Vocab < 45Grammar
'''

class EAnalyze:
  def __init__(self, text) -> None:
    self.text = text
    self.score_weights = {
      "relevance": 0.2,
      "vocab": 0.35,
      "grammar": 0.45
    }

    self.actual_score = {
      "relevance": 0,
      "vocab": 0,
      "grammar": 0
    }
    self.models = {
      "relevance": RelevanceAnalyzer(),
      "vocab": VocabularyAnalyzer(),
      "grammar": GrammarChecker()
    }

    self.preprocessor = TextProcessor()

  

  def analyze(self):
    self.sentences = self.preprocessor.process(self.text)
    model_threads = []
    def __process(model_name):
      self.actual_score[model_name] = self.models[model_name].process(self.sentences)
    for model_name in self.models.keys():
      model_thread = Thread(target=__process, args=(model_name,))
      model_thread.start()
      model_threads.append(model_thread)

    for thread in model_threads:
      thread.join()
  
  def score(self):
    self.analyze()
    score = 0
    print(self.actual_score)
    for model_name in self.score_weights.keys():
      score += self.actual_score[model_name] * self.score_weights[model_name]
    # Add booster marks if grammar or vocab is above 90
    if self.score_weights["vocab"] > 90 or self.score_weights["grammar"] > 90:
      score += 11 # 11 bonus for extraordinary
    if self.score_weights["vocab"] > 85 or self.score_weights["grammar"] > 85:
      score += 6 # 11 bonus for extraordinary
    return score
    
    
    





