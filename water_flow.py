import RPi.GPIO as GPIO
import time,sys, datetime
import psycopg2
from psycopg2.extras import execute_values

'''
Configure raspberry
'''

GPIO.setmode(GPIO.BCM)
inpt = 26
GPIO.setup(inpt,GPIO.IN)

'''
Configure some global variables
'''

current_input = GPIO.input(inpt)                        # This is used to compare to the new_input later.
total_rotations = 0                                     # This is a counter. It gets reset after the number of seconds in rotation_downtime.
cup_movements = 200                                     # This is how many rotations occur as a cup of liquid passes through.
rotation_downtime = 5                                   # Sets the cut-off time for establishing a water-flow event.
last_movement_time = time.time() + rotation_downtime    # This is used to determine if a new water-flow event should be created.
record_data = False                                     # A flag used to trigger database insert.

data = []

'''
Enter database credentials here. I recommend the free-tier Postgres databses from Heroku which allow up to 10k rows. heroku.com
But you can use any Postgres db - have not tested with other dbs.
'''

host=""
database=""
user="" 
password=""

print('Control C to exit')

def commit_data(conn, data):

    '''
    This passes data to the data base as a single row. It then resets/empties data.
    '''

    cur = conn.cursor()
    insert_statement = "INSERT INTO flow_meter ('datetime','movements','cups','gallons') VALUES %s".replace("'",'')
    execute_values(cur,insert_statement,data)
    conn.commit()
    print ('Data sent.')
    cur.close()
    data = []
    return data

def prep_and_send(data,total_rotations):

    '''
    Calculates measurements (cups and gallons). Prepares the data into a database-friendly tuple. Appends that tuple to a list. 
    
    It then tries to connect to database. If it is not successful then it does nothing but saves the data; it will try to send 
    the list of data-tuples the next time there is a water-flow event. 
    
    Once the connection is successful data is emptied in commit_data().
    '''

    total_cups = total_rotations/cup_movements
    total_gallons = total_cups/16
    now = datetime.datetime.now() 
    print('{}: Movements: {}. \nCups: {}. \nGallons: {}'.format(now,total_rotations,total_cups,total_gallons))

    current_data = (
        now,
        round(total_rotations,2),
        round(total_cups,2),
        round(total_gallons,2), 
        )
    data.append(current_data)
    try:                
        '''
        Establish connection with Db and try to insert.
        '''
        conn = psycopg2.connect(host = host, database = database, user = user, password = password)
        data = commit_data(conn, data)			
        conn.close()
    except psycopg2.OperationalError as e:
        '''In case of error does not reset data to [] (see commit_data).'''
        e = e + '\n' + e.__traceback__
        print (e)                      
    return data

while True:

    '''
    This is what actually runs the whole time. 
    It first checks to see if new_input is different from current_input. This would be the case if there was a rotation.
    Once it detects that the input is different it knows water is flowing.
    It starts tracking the total_rotations and when the last rotation occured. 

    After each rotation it refreshes the value of the last rotation time.

    It waits a few seconds (rotation_downtime) after the last rotation time to make sure the water has stopped. 
    Once the water stops it passes the total_rotations to prep_and_send(). 
    It also passes 'data' which is any previous water-flow events that were not successfully sent at the time they were recorded.
    '''

    new_input = GPIO.input(inpt)
    if new_input != current_input:
        total_rotations += 1
        if time.time() <= last_movement_time: #if it hasn't been more than 10 seconds
            record_data = True
            current_input = new_input
            last_movement_time = time.time() + rotation_downtime
        else: #flow starts
            last_movement_time = time.time() + rotation_downtime

    elif record_data == True and time.time() > last_movement_time: #if it's been x seconds since last change
        data = prep_and_send(data,total_rotations)
        record_data = False
        total_rotations = 0
        last_movement_time = time.time() + rotation_downtime
        current_input = new_input

'''
This last part simply prints some helpful information. It also allows for a clean exit if user presses Ctrl + C.
'''

    try:
        print('New input: ',new_input, '. Current input: ', current_input, '. Movements: ', total_rotations)
    except KeyboardInterrupt:
        print('\nCTRL C - Exiting nicely')
        GPIO.cleanup()
        sys.exit()
