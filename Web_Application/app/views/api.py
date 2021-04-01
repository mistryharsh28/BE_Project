# import random
# import string
from flask import Blueprint
# from flask_mysqldb import MySQL
# from passlib.hash import sha256_crypt as sha
# from flask_session import Session
from flask import jsonify
from app import *
from time import sleep

# Text processing libraries
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import yake
from heapq import nlargest

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/get_rooms_data/<user_email>', methods=['GET', 'POST'])
def get_rooms_data(user_email):

    # provides data for all rooms attended by the given user
    # Try the links below while running locally
    # http://127.0.0.1:8000/api/get_rooms_data/mistryharsh28@gmail.com
    # http://127.0.0.1:8000/api/get_rooms_data/atharva1111@gmail.com


    rooms = mongo.db.rooms.find({"members_attended": str(user_email), 'active': False}) # active False means the meetings which are already done and currently not active
    result = []
    room_ids_removed = []
    for room in rooms:
        r = {}
        r['_id'] = str(room['_id'])
        r['members'] = room['members']
        r['members_attended'] = room['members_attended']
        r['room_id'] = room['room_id']
        r['created_by_user'] = room['created_by_user']
        r['active'] = room['active']
        r['start_date_time'] = room['start_date_time']
        r['end_date_time'] = room['end_date_time']
        r['transcripts'] = []
        transcripts = mongo.db.transcripts.find({"room_id": room['room_id']})
        for transcript in transcripts:
            r['transcripts'].append((str(transcript['spoken_by_user']), str(transcript['transcript'])))
        result.append(r)
        
    return jsonify({'rooms_count': rooms.count(),'rooms': result})



def analysis_of_room(user_email, room_id, language, number_of_keywords, percentage_of_summarization):
    
    #check analysis already exists or not
    analysis = mongo.db.analysis.find({"room_id": room_id})
    for a in analysis:
        return
    
    print("Analysis for", room_id)
    # Collect the transcripts of room
    whole_transcript = ""
    transcripts = mongo.db.transcripts.find({"room_id": room_id})
    for transcript in transcripts:
        whole_transcript = "{}{}.".format(whole_transcript, transcript["transcript"])

    # Text summarization
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(whole_transcript)
    sentence_tokens = [sent for sent in doc.sents]
    select_length = int(len(sentence_tokens)*percentage_of_summarization)

        # Using Yake
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = number_of_keywords

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(whole_transcript)
    keywords_list = []
    sentence_scores1 = {}
    for sent in sentence_tokens:
        for key in keywords:
            if key[0].lower() in sent.text.lower():
                if sent not in sentence_scores1.keys():
                    sentence_scores1[sent] = (1 - key[1])
                else:
                    sentence_scores1[sent] += (1 - key[1])                 

    for key in keywords:
        keywords_list.append(key[0])

    summary1 = nlargest(select_length, sentence_scores1, key = sentence_scores1.get)

    final_summary = [word.text for word in summary1]
    for i in range(len(final_summary)):
        final_summary[i] = final_summary[i][0].upper() + final_summary[i][1:]
    summary1 = ' '.join(final_summary)

    mongo.db.analysis.insert_one({"room_id": room_id, "keywords": keywords_list, "summarized_text": summary1})


@api.route('/start_analysis_of_room/<user_email>/<room_id>/<language>/<number_of_keywords>/<percentage_of_summarization>', methods=['GET', 'POST'])
def start_analysis_of_room(user_email, room_id, language, number_of_keywords, percentage_of_summarization):
    
    # http://127.0.0.1:8000/api/start_analysis_of_room/mistryharsh28@gmail.com/fghdrhbrserhb31342543
    # Run and see the command prompt 

    @app.after_response
    def after_sending_response():
        # This thing is done so that if the analysis part takes time the client application making 
        # the request does not have to wait for it to complete. Also we do not need to deal with 
        # timeouts

        # Do the analysis and saving of the data here.
        analysis_of_room(user_email, room_id, language, int(number_of_keywords), float(percentage_of_summarization))

    return jsonify({"status": 'success'})
    