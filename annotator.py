import json
import sqlite3
from typing import Dict
import nltk

from zeyrek import MorphAnalyzer

MAX_SIZE = 2000
nltk.download('punkt')

class Annotator:
    DICTIONARY_FILE = 'dictionary.json'
    def __init__(self, MAX_TEXT_SIZE=MAX_SIZE):
        self.MAX_TEXT_SIZE = MAX_TEXT_SIZE
        self.dictionary = json.load(open(Annotator.DICTIONARY_FILE, 'r', encoding='utf-8'))
        self.analyzer = MorphAnalyzer()
    
    def annotate(self, text: str) -> Dict:
        # Analyze in Zeyrek
        # look up lemmas in dictionary
        # send as json
        analyzed = self._analyze_text(text)
        annotated = []
        for paragraph in analyzed:
            annotated_paragraph = []
            for i, word in enumerate(paragraph):
                term, lemmas = word
                lemmas = [{ lemma: self.dictionary.get(lemma, []) } for lemma in lemmas]
                # If there are more than one lemmas for a word, 
                # we remove values that don't have definitions (eg. for tanesi: tane-tanes)
                if len(lemmas) > 1:
                    lemmas = [lemma for lemma in lemmas if any(lemma.values())]
                annotated_word = { 'id': i+1, 'word': term, 'meanings': lemmas}
                annotated_paragraph.append(annotated_word)
            annotated.append(annotated_paragraph)
        return annotated

    def _analyze_text(self, text: str) -> Dict:
        """
        Cuts the text after MAX_TEXT_SIZE (without cutting the last word)
        Splits the text into paragraphs
        Splits the paragraphs into sentences
        """
        if len(text) > self.MAX_TEXT_SIZE:
            last_index = text[:self.MAX_TEXT_SIZE].rfind(' ')
            text = text[:last_index]
        paragraphs = text.split('\n')
        analyzed = []
        for paragraph in paragraphs:
            lemmatized_tuples = self.analyzer.lemmatize(paragraph)
            lemmatized_paragraph = []
            # Convert tuples into dictionaries
            # Proper names are given as a different word, yet we only 
            # need the lower case, so we'll count them as one lemma
            for tuple_ in lemmatized_tuples:
                lemmas = list(set([ _.lower() for _ in tuple_[1]]))
                lemmatized_paragraph.append((tuple_[0], lemmas))
            analyzed.append(lemmatized_paragraph)
        return analyzed


if __name__ == '__main__':
    with open('text.txt', encoding='utf-8') as text_file:
        text_content = text_file.read()
        annotator = Annotator()
        annotator.annotate(text_content)
