import numpy as np
import nltk
import spacy
from transformers import pipeline


class SentimentAnalyzer:
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_analysis = pipeline("sentiment-analysis")

    def split_text_to_sentences(self, text, max_words=50):
        sentences = nltk.sent_tokenize(text)  # Tokenize text into sentences
        
        result_sentences = []
        current_sentence = []

        for sentence in sentences:
            words = nltk.word_tokenize(sentence)  # Tokenize sentence into words

            if len(current_sentence) + len(words) <= max_words:
                current_sentence.extend(words)
            else:
                result_sentences.append(" ".join(current_sentence))
                current_sentence = words
        
        # Add the last sentence
        if current_sentence:
            result_sentences.append(" ".join(current_sentence))
        
        return result_sentences

    def preprocess_text(self, text):
        # Use SpaCy for text preprocessing
        doc = self.nlp(text)
        # Lemmatize and remove stop words
        cleaned_text = " ".join([token.lemma_ for token in doc if not token.is_stop])
        return cleaned_text

    def analyze_sentiment(self, text):
        # Preprocess the text
        cleaned_text = self.preprocess_text(text)
        sentences = self.split_text_to_sentences(cleaned_text, 400)
        # Perform sentiment analysis
        scores = 0
        for sentence in sentences:
          sentiment_results = self.sentiment_analysis(sentence)
          for result in sentiment_results:
            scores += -abs(result["score"]) if result["label"] == "NEGATIVE" else result["score"]
        return scores/len(sentences)

    def analyze(self, sentences):
      results = []
      for i,sentence in enumerate(sentences):
        sentiment_score = self.analyze_sentiment(sentence)
        results.append({"score": sentiment_score, "sentence": sentence})

      spikes = self.find_spikes(results, 1.6)
      return spikes

    def find_spikes_iqr(self, values):
        # Calculate Q1 (25th percentile) and Q3 (75th percentile)
        Q1 = np.percentile(values, 25)
        Q3 = np.percentile(values, 75)
        # Calculate IQR
        IQR = Q3 - Q1
        # Define bounds for outliers
        lower_bound = Q1 - 0.1 * IQR
        upper_bound = Q3 + 0.1 * IQR

        # Identify spikes
        spikes = [(i, value) for i, value in enumerate(values) if value < lower_bound or value > upper_bound]
        return spikes


    def find_spikes(self, values, threshold=2):
        spikes = {}
        std = np.std([value["score"] for value in values])
        for i in range(1, len(values) - 1):
            prev_diff = abs(values[i]["score"] - values[i - 1]["score"])
            next_diff = abs(values[i]["score"] - values[i + 1]["score"])
            if prev_diff > 2 * std and next_diff > threshold * std:
                spikes[(i, values[i]["sentence"])] = None
        return spikes
