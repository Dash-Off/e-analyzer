from eanalyze.vocabulary_analyzer import VocabularyAnalyzer
from eanalyze.text_processor import TextProcessor
from eanalyze.relevance_analyzer import RelevanceAnalyzer
from eanalyze.grammar_checker import GrammarChecker
from eanalyze.sentiment_analyzer import SentimentAnalyzer
from threading import Thread
from enum import Enum


class CORRECTION_TYPE(Enum):
  SENTI = 1
  READ = 2
  GRAMMAR = 3

db_correction_type_mapping = {
  "sentiment": CORRECTION_TYPE.SENTI.name,
  "easeness": CORRECTION_TYPE.READ.name,
  "structure": CORRECTION_TYPE.GRAMMAR.name,
}

class CORRECTION_SUB_TYPE(Enum):
  INS = 1
  UPDATE = 2

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
    self.sentiment_processor = SentimentAnalyzer()

    self.preprocessor = TextProcessor()
    self.sentences = self.preprocessor.process(self.text)

  

  def analyze(self):
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
    for model_name in self.score_weights.keys():
      score += self.actual_score[model_name] * self.score_weights[model_name]
    # Add booster marks if grammar or vocab is above 90
    if self.score_weights["vocab"] > 90 or self.score_weights["grammar"] > 90:
      score += 11 # 11 bonus for extraordinary
    if self.score_weights["vocab"] > 85 or self.score_weights["grammar"] > 85:
      score += 6 # 11 bonus for extraordinary
    return score

  def extras(self):
    return {
      "sentiment": self.sentiment_processor.analyze(sentences=self.sentences),
      "easeness": self.models["vocab"].easeness_scores,
      "structure": self.models["grammar"].changes
    }
  
  def get_corrections(self):
    corrections = []
    extras = self.extras()
    for analysis_part in extras:
      type = db_correction_type_mapping[analysis_part]
      for key, value in extras[analysis_part].items():
        index = key[0]
        sentence = key[1]
        suggestion = {}
        if type == CORRECTION_TYPE.GRAMMAR.name:
          for val in value:
            suggestion["replacement"] = val[4]
            suggestion["pos"] = val[2]
            suggestion["actual"] = val[1]
            suggestion["correctionSubType"] = CORRECTION_SUB_TYPE.INS.name if val[2] == val[3] else CORRECTION_SUB_TYPE.UPDATE.name
            correction = {
              "correctionType": type,
              "suggestion": suggestion,
              "line": index,
              "actual": sentence
            }
            corrections.append(correction)
        else:
          correction = {
            "correctionType": type,
            "suggestion": suggestion,
            "line": index,
            "actual": sentence
          }
          corrections.append(correction)
    return corrections
  
  def get_result_payload(self):
    final_score = self.score()
    return {
      "overallScore": final_score,
      "grammarScore": self.actual_score["grammar"],
      "structureScore": self.actual_score["relevance"],
      "vocabScore": self.actual_score["vocab"],
      "corrections": self.get_corrections(),
    }

    



    





