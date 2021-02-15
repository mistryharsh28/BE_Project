# import random
# import string
from flask import Blueprint
# from flask_mysqldb import MySQL
# from passlib.hash import sha256_crypt as sha
# from flask_session import Session
from flask import jsonify
from app import *
from time import sleep

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



def analysis_of_room(user_email, room_id):
    # Collect the transcripts of room
    # Text summarization
    # Keywords 
    
    # Sample code to test working
    print(user_email, room_id)
    for i in range(20):
        sleep(1)
        print(i)
        print('This is working after the response has been sent for the request. Haha.')



@api.route('/start_analysis_of_room/<user_email>/<room_id>', methods=['GET', 'POST'])
def start_analysis_of_room(user_email, room_id):
    
    # http://127.0.0.1:8000/api/start_analysis_of_room/mistryharsh28@gmail.com/fghdrhbrserhb31342543
    # Run and see the command prompt 

    print('Start')

    @app.after_response
    def after_sending_response():
        # This thing is done so that if the analysis part takes time the client application making 
        # the request does not have to wait for it to complete. Also we do not need to deal with 
        # timeouts

        # Do the analysis and saving of the data here.
        analysis_of_room(user_email, room_id)

    print('Done')    

    return jsonify({"status": 'success'})
    