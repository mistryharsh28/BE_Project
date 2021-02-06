# import random
# import string
from flask import Blueprint
# from flask_mysqldb import MySQL
# from passlib.hash import sha256_crypt as sha
# from flask_session import Session
from flask import jsonify
from app import *


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/get_rooms_data/<user_email>', methods=['GET', 'POST'])
def get_rooms_data(user_email):
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