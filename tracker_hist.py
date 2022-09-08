import sqlite3
from sqlite3 import Error
import time

(
    NO_CHANGES,
    NEW,
    UPDATED
) = range(3)

def create_table():
    sql_create_table = """ CREATE TABLE IF NOT EXISTS message (
                                        id text PRIMARY KEY,
                                        message text NOT NULL,
                                        ts integer
                                    ); """

    with sqlite3.connect("sqlite.db") as db:
        cursor = db.cursor()
        cursor.execute(sql_create_table)
        db.commit()


def insert_new_message(message_id, message):

    sql = ''' INSERT INTO message (id,message,ts)
                  VALUES(?,?,?) '''
    with sqlite3.connect("sqlite.db") as db:
        cursor = db.cursor()
        cursor.execute(sql, (message_id, message, int(time.time())))
        db.commit()


def update_message(message_id, message):
    sql = '''
        update message set message = ?, ts=? where id = ?;
        '''
    with sqlite3.connect("sqlite.db") as db:
        cursor = db.cursor()
        cursor.execute(sql, ( message, int(time.time()), message_id))
        db.commit()


def generate_id(*args):
    return hash('blahblahblah'.join(args))


def check_subscribe(uid, message):
    # uid = generate_id(uid)
    with sqlite3.connect("sqlite.db") as db:
        cursor = db.cursor()
        cursor.execute(f'select * from message where id = "{uid}"')
        data = cursor.fetchone()
        if data is None:
            insert_new_message(uid, message)
            return NEW
        else:
            if message != data[1]:
                update_message(uid, message)
                return UPDATED
            else:
                return NO_CHANGES




if __name__ == '__main__':
    # create_table()
    # insert_new_message('asdfasdf', 'asdfhiwuefhiwieu')
    check_subscribe('asdfasdf', '124')
    check_subscribe('asdfa12sdfaa', 'asdffoiw')