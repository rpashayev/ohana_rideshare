from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash, session
import re

MSG_REGEX = re.compile(r'^\s*$')

class Message:
    DB = 'rideshare_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.sender = None

    
    @classmethod
    def send_message(cls, data):
        query = '''
            INSERT 
            INTO messages(content, sender_id, ride_id)
            VALUES ( %(content)s,  %(sender_id)s, %(ride_id)s );
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)

    
    @staticmethod
    def validate_message(message):
        is_valid = True
        if len(message['content']) == 0 or MSG_REGEX.match(message['content']):
            flash('Message cannot be empty!', 'msg_error')
            is_valid = False

        return is_valid
    