from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RelevanceAnalyzer:
  '''
  Add relevance based on RAKE category of question and answer
  Add relevence between paragraphs
  Get datasets of topics and relevant words populated in the document
  '''
  def __init__(self) -> None:
    self.model = TfidfVectorizer(stop_words='english')
  
  def get_line_number(self, percent, total):
    return (percent * total) // 100

  def get_partitioning(self, sentences):
    total = len(sentences)
    if len(sentences) == 1:
      return [sentences, sentences, sentences]
    
    if len(sentences) == 2:
      return [[sentences[0]], [sentences[1]], [sentences[1]]]
    if len(sentences) == 3:
      return [[sentences[0]], [sentences[1]], [sentences[2]]]
    if len(sentences) == 4:
      return [[sentences[0]], [sentences[1], sentences[2]], sentences[3]]
    else:
      intro_start, intro_end = 0, self.get_line_number(15, total)
      body_start, body_end = intro_end, self.get_line_number(80, total)
      conclusion_start, conclusion_end = body_end, total
      return [sentences[intro_start:intro_end], sentences[body_start:body_end], sentences[conclusion_start: conclusion_end]]

  def get_relevence_score(self, textA, textB):
    documents = [textA, textB]
    
    tfidf_matrix = self.model.fit_transform(documents)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim[0][0] * 1000

  def get_body_conclusion_relevance(self, body, conclusion):
    return self.get_relevence_score("".join(body), "".join(conclusion))

  def get_intro_body_first_relevance(self, body, intro):
    '''Get relevance of 30% of body to introduction given'''
    return self.get_relevence_score("".join(intro), "".join(body[0: self.get_line_number(30, len(body))]))
  
  def get_intro_conclusion_relevance(self, conclusion, intro):
    return self.get_relevence_score("".join(conclusion), "".join(intro))

  def get_text_and_question_relevance(self):
    pass

  def process(self, sentences):
    self.sentences = []
    self.total = len(sentences)
    # Use all relevance and average
    intro, body, conclusion = self.get_partitioning(sentences)
    print("Intro:"+"".join(intro))
    print("Body:"+"".join(body))
    print("Conclusion:"+"".join(conclusion))

    print("IntroBodyfirst" + str(self.get_intro_body_first_relevance(body, intro)))
    print("BodyConclusion" + str(self.get_body_conclusion_relevance(intro + body, conclusion)))
    print("IntroConclusion" + str(self.get_intro_conclusion_relevance(conclusion, intro)))
    return (
      0.2 * min(self.get_intro_body_first_relevance(body, intro), 100) +
      0.3 * min(2* self.get_body_conclusion_relevance(intro + body, conclusion), 100) + # Amplify the conclusion and body relevance
      0.5 * min(self.get_intro_conclusion_relevance(conclusion, intro), 100)
    )


    