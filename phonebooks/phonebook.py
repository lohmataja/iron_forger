__author__ = 'Liuda'
import os, sys
import sqlite3

def exists(entry, field, db, cursor):
    return cursor.execute("SELECT * FROM {} WHERE {}=? LIMIT 1".format(db, field), (entry, )).fetchone() != None

def create(cursor, phonebook):
    cursor.execute('CREATE TABLE IF NOT EXISTS pb_data (name TEXT, phone_number TEXT, pb_id INTEGER, UNIQUE (name, pb_id) ON CONFLICT FAIL )')
    cursor.execute('CREATE TABLE IF NOT EXISTS pb_registry (name TEXT, UNIQUE (name) ON CONFLICT FAIL )')
    try:
        cursor.execute("INSERT INTO pb_registry VALUES (?)", (phonebook, ))
        print('{} created!'.format(phonebook))
    except sqlite3.IntegrityError:
        print('Error: {} already exists!'.format(phonebook))

def add(cursor, name, phone_number, phonebook):
    #check that phonebook exists
    if not exists(phonebook, 'pb_name', 'pb_registry', cursor):
        user_input = input("{} doesn't exist. Would you like to create it? (Y to create)".format(phonebook)).lower()
        if user_input == 'y':
            create(cursor, phonebook)
        else:
            print("Command cancelled")
            return
    #check whether entry exists
    if not exists(name, 'name', phonebook, cursor):
        cursor.execute("INSERT INTO pb_data VALUES (?, ?, ?)", (name, phone_number, phonebook))
        print('Added {} to {}'.format(name, phonebook))
        return True
    else:
        print('Error: {} already exists in {}. Use the "update" command.'.format(name, phonebook))
        return False

def update(name, phone_number, filename, phonebook):
    print('Updated an entry')
    try:
        print('Previous entry:')
        print(name, phonebook[name])
    except:
        print('Previous entry not found.')
    phonebook[name] = phone_number
    print('New entry:')
    print(name+'\t'+phonebook[name])

def lookup(cursor, name, phonebook, field='name'):
    if exists(name, 'name', phonebook, cursor):
        phone_number = cursor.execute("SELECT * FROM {} WHERE {} IN '{}'".format(
            phonebook, field, name)).fetchall()
        for p in phone_number:
            print(p)
        # print("{}: {}".format(phone_number))
    else:
        print("Error: entry {} not found in {|".format(name, phonebook))

def reverse_lookup(cursor, name, phonebook):
    lookup(cursor, name, phonebook, field='phone_number')

def remove(cursor, name, phonebook):
    # if exists(name, 'name', 'pb_data')
    pass

if __name__ == '__main__':
    #parse arguments
    args = sys.argv[1:]
    command = args.pop(0)
    #open the database
    db_conn = sqlite3.connect('./phonebook.db')
    cursor = db_conn.cursor()
    #dispatch the command
    dispatch = {'create':create,
                'add':add,
                'update':update,
                'lookup':lookup,
                'reverse_lookup':reverse_lookup,
                'remove':remove}
    dispatch[command](cursor, *args)
    #save changes, exit
    db_conn.commit()
    db_conn.close()

# db_conn = sqlite3.connect('./phonebook.db')
# c = db_conn.cursor()