import re

class TextProcessor:
  def __init__(self) -> None:
    self.sentence_regex = r'[^.]*\.+(?!\.)'
  def get_by_regex(self, input_text):
    '''Provides all the sentences using regex in given input paragraph'''
    return re.findall(self.sentence_regex, input_text)

  def process(self, input_text):
    '''Process operation on input text can include in future pre-processing'''
    return self.get_by_regex(input_text=input_text)

