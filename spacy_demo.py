import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import yake

text = """Women education is a catch all term which refers to the state of primary, secondary, tertiary and health education in girls and women. There are 65 Million girls out of school across the globe; majority of them are in the developing and underdeveloped countries. All the countries of the world, especially the developing and underdeveloped countries must take necessary steps to improve their condition of female education; as women can play a vital role in the nation’s development.
If we consider society as tree, then men are like its strong main stem which supports the tree to face the elements and women are like its roots; most important of them all. The stronger the roots are the bigger and stronger the tree will be spreading its branches; sheltering and protecting the needy.
Women are the soul of a society; a society can well be judged by the way its women are treated. An educated man goes out to make the society better, while an educated woman; whether she goes out or stays at home, makes the house and its occupants better.
Women play many roles in a society- mother, wife, sister, care taker, nurse etc. They are more compassionate towards the needs of others and have a better understanding of social structure. An educated mother will make sure that her children are educated, and will weigh the education of a girl child, same as boys.
History is replete with evidences, that the societies in which women were treated equally to men and were educated; prospered and grew socially as well as economically. It will be a mistake to leave women behind in our goal of sustainable development, and it could only be achieved if both the genders are allowed equal opportunities in education and other areas.
Education makes women more confident and ambitious; they become more aware of their rights and can raise their voice against exploitation and violence. A society cannot at all progress if its women weep silently. They have to have the weapon of education to carve out a progressive path for their own as well as their families."""

stopwords = list(STOP_WORDS)

nlp = spacy.load('en_core_web_sm')

doc = nlp(text)

punctuation = punctuation + '\n'


word_frequencies = {}
for word in doc:
    if word.text.lower() not in stopwords:
        if word.text.lower() not in punctuation:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1
                
print(word_frequencies)

sentence_tokens = [sent for sent in doc.sents]
print(sentence_tokens)

from heapq import nlargest
select_length = int(len(sentence_tokens)*0.3)
select_length
max_frequency = max(word_frequencies.values())





# Maximum Frequency method
for word in word_frequencies.keys():
    word_frequencies[word] = word_frequencies[word]/max_frequency
        
sentence_scores = {}
for sent in sentence_tokens:
    for word in sent:
        if word.text.lower() in word_frequencies.keys():
            if sent not in sentence_scores.keys():
                sentence_scores[sent] = word_frequencies[word.text.lower()]
            else:
                sentence_scores[sent] += word_frequencies[word.text.lower()]

summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
final_summary = [word.text for word in summary]
summary = ' '.join(final_summary)
summary





# Using Yake
language = "en"
max_ngram_size = 3
deduplication_thresold = 0.9
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = len(word_frequencies) // 2

custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
keywords = custom_kw_extractor.extract_keywords(text)

sentence_scores1 = {}
for sent in sentence_tokens:
    for key in keywords:
        if key[0].lower() in sent.text.lower():
            if sent not in sentence_scores1.keys():
                sentence_scores1[sent] = key[1]
            else:
                sentence_scores1[sent] += key[1] 
                

summary1 = nlargest(select_length, sentence_scores1, key = sentence_scores1.get)

final_summary = [word.text for word in summary1]
summary1 = ' '.join(final_summary)
summary1





# Using Similarity of Spacy model
similarity_words = {}
user_input_word = nlp("females")
for word in doc:
    if word.text.lower() not in stopwords:
        if word.text.lower() not in punctuation:
            if word.text not in similarity_words.keys():
                similarity_words[word.text] = user_input_word[0].similarity(nlp(word.text))
                
sentence_scores2 = {}
for sent in sentence_tokens:
    for word in sent:
        if word.text.lower() in similarity_words.keys():
            if sent not in sentence_scores2.keys():
                sentence_scores2[sent] = similarity_words[word.text]
            else:
                sentence_scores2[sent] += similarity_words[word.text] 
                
summary2 = nlargest(select_length, sentence_scores2, key = sentence_scores2.get)
final_summary = [word.text for word in summary2]
summary2 = ' '.join(final_summary)
summary2




text
summary # Maximum frequency normalization
summary1 # Using score of YAKE
summary2 # Using sematic similarity of spacy model