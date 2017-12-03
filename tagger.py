from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

import os

os.environ['CLASSPATH'] = "/home/sunil/project/FBChatbot/stanford-ner"
os.environ['STANFORD_MODELS'] = "/home/sunil/project/FBChatbot/stanford-ner/classifiers"

def TagDetection(text):

    st = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz')

    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)
    return classified_text