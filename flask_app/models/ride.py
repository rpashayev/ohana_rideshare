from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import message, user
from flask import flash
import re, datetime

RIDE_REGEX = re.compile(r'^\s*$')

class Ride:
    DB = 'rideshare_schema'
    
    def __init__(self, data):
        self.id = data['id']
        self.destination = data['destination']
        self.pickup = data['pickup']
        self.ride_date = data['ride_date']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.driver = None
        self.rider = None
        self.messages = []
    
    @classmethod
    def get_all_rides(cls):
        all_rides = []
        query = '''
            SELECT *
            FROM rides
            LEFT JOIN users AS drivers ON drivers.id = rides.driver_id
            LEFT JOIN users AS riders ON riders.id = rides.rider_id
            ORDER BY rides.created_at DESC;
        '''
        results = connectToMySQL(cls.DB).query_db(query)

        for row in results:
            ride = cls(row)
            driver_info = {
                'id': row['drivers.id'],
                'first_name': row['drivers.first_name'],
                'last_name': row['drivers.last_name'],
                'email': row['drivers.email'],
                'password': row['drivers.password'],
                'created_at': row['drivers.created_at'],
                'updated_at': row['drives.updated_at']
            }
            ride.driver = user.User(driver_info)
    
            rider_info = {
                'id': row['riders.id'],
                'first_name': row['riders.first_name'],
                'last_name': row['riders.last_name'],
                'email': row['riders.email'],
                'password': row['riders.password'],
                'created_at': row['riders.created_at'],
                'updated_at': row['riders.updated_at']
            }
            ride.rider.append(user.User(rider_info))
            all_rides.append(ride)
        return all_rides
    
    @classmethod
    def save_ride(cls, data):
        query = '''
            INSERT 
            INTO rides(destination, pickup, ride_date, details, rider_id)
            VALUES ( %(destination)s, %(pickup)s, %(ride_date)s, %(details)s, %(rider_id)s );
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete_ride(cls, data):
        query = '''
            DELETE
            FROM rides
            WHERE id = %(id)s;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def edit_ride(cls, data):
        query = '''
            UPDATE rides
            SET destination=%(destination)s, pickup=%(pickup)s, ride_date=%(ride_date)s, details=%(details)s
            WHERE id = %(id)s;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def one_booked_ride(cls, data):
        query = '''
            SELECT *
            FROM rides
            LEFT JOIN users AS riders ON riders.id = rides.rider_id
            LEFT JOIN users AS drivers ON drivers.id = rides.driver_id
            LEFT JOIN messages ON messages.ride_id = rides.id
            LEFT JOIN users AS senders ON senders.id = messages.sender_id
            WHERE rides.id = %(id)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)

        one_ride = cls(results[0])
            
        rider_info = {
            'id': results[0]['riders.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['riders.created_at'],
            'updated_at': results[0]['riders.updated_at']
        }
        one_ride.rider = user.User(rider_info)
        
        driver_info = {
        'id': results[0]['drivers.id'],
        'first_name': results[0]['drivers.first_name'],
        'last_name': results[0]['drivers.last_name'],
        'email': results[0]['drivers.email'],
        'password': results[0]['drivers.password'],
        'created_at': results[0]['drivers.created_at'],
        'updated_at': results[0]['drivers.updated_at']
        }
        one_ride.driver = user.User(driver_info)
        
        for row in results:
            if row['senders.id']:
                sender_info = {
                    'id': row['senders.id'],
                    'first_name': row['senders.first_name'],
                    'last_name': row['senders.last_name'],
                    'email': row['senders.email'],
                    'password': row['senders.password'],
                    'created_at': row['senders.created_at'],
                    'updated_at': row['senders.updated_at']
                }
                message_info = {
                    'id': row['messages.id'],
                    'content': row['content'],
                    'created_at': row['messages.created_at'],
                    'updated_at': row['messages.updated_at'],
                    'sender_id': user.User(sender_info)
                }
                one_ride.messages.append(message_info)
                
        return one_ride
    
    @classmethod
    def booked_rides(cls):
        all_booked_rides = []
        query = '''
            SELECT *
            FROM rides
            LEFT JOIN users AS drivers ON drivers.id = rides.driver_id
            LEFT JOIN users AS riders ON riders.id = rides.rider_id
            WHERE driver_id IS NOT NULL
            ORDER BY rides.created_at DESC;
        '''
        results = connectToMySQL(cls.DB).query_db(query)

        for row in results:
            ride = cls(row)
            driver_info = {
                'id': row['drivers.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            ride.driver = user.User(driver_info)
    
            rider_info = {
                'id': row['riders.id'],
                'first_name': row['riders.first_name'],
                'last_name': row['riders.last_name'],
                'email': row['riders.email'],
                'password': row['riders.password'],
                'created_at': row['riders.created_at'],
                'updated_at': row['riders.updated_at']
            }
            ride.rider = user.User(rider_info)
            all_booked_rides.append(ride)
        return all_booked_rides
    
    @classmethod
    def one_requested_ride(cls, data):
        query = '''
            SELECT *
            FROM rides
            LEFT JOIN users AS riders ON riders.id = rides.rider_id
            WHERE rides.id = %(id)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query, data)

        one_ride = cls(results[0])

        rider_info = {
            'id': results[0]['riders.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['riders.created_at'],
            'updated_at': results[0]['riders.updated_at']
        }
        one_ride.rider = user.User(rider_info)
        
        return one_ride
    
    @classmethod
    def requested_rides(cls):
        all_requested_rides=[]
        query = '''
            SELECT *
            FROM rides
            LEFT JOIN users AS riders ON riders.id = rides.rider_id
            WHERE driver_id IS NULL
            ORDER BY rides.created_at DESC;
        '''
        results = connectToMySQL(cls.DB).query_db(query)

        for row in results:
            ride = cls(row)
    
            rider_info = {
                'id': row['riders.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['riders.created_at'],
                'updated_at': row['riders.updated_at']
            }
            ride.rider = user.User(rider_info)
            all_requested_rides.append(ride)
            
        return all_requested_rides
    
    @classmethod
    def add_driver_to_ride(cls, data):
        query = '''
            UPDATE rides
            SET driver_id = %(driver_id)s
            WHERE id=%(id)s;
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def remove_driver_from_ride(cls, data):
        query = '''
            UPDATE rides
            SET driver_id = NULL
            WHERE id=%(id)s;
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_ride(ride):
        is_valid = True
        if len(ride['destination']) == 0 or RIDE_REGEX.match(ride['destination']):
            flash('Destination cannot be empty!', 'ride_error')
            is_valid = False
        if len(ride['pickup']) == 0 or RIDE_REGEX.match(ride['pickup']):
            flash('Pickup location cannot be empty!', 'ride_error')
            is_valid = False
        if len(ride['details']) == 0 or RIDE_REGEX.match(ride['details']):
            flash('Please add details', 'ride_error')
            is_valid = False
        if not ride['ride_date']:
            flash('Invalid date!', 'ride_error')
            is_valid = False
        elif datetime.datetime.strptime(ride['ride_date'],'%Y-%m-%d') < datetime.datetime.now():
            flash('Cannot be past date', 'ride_error')
            is_valid = False
            
        return is_valid

    @staticmethod
    def validate_ride_edit(ride):
        is_valid = True
        if len(ride['pickup']) == 0 or RIDE_REGEX.match(ride['pickup']):
            flash('Pickup location cannot be empty!', 'ride_error')
            is_valid = False
        if len(ride['details']) == 0 or RIDE_REGEX.match(ride['details']):
            flash('Please add details', 'ride_error')
            is_valid = False
            
        return is_valid