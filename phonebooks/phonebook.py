__author__ = 'Liuda'
import sqlite3
import sys

def pb_id(cursor, phonebook):
    return cursor.execute("SELECT ROWID FROM pb_registry WHERE name=?", (phonebook, )).fetchone()[0]

def create(cursor, phonebook):
    cursor.execute('CREATE TABLE IF NOT EXISTS pb_data (name TEXT, phone_number TEXT, pb_id INTEGER, UNIQUE (name, pb_id) ON CONFLICT FAIL )')
    cursor.execute('CREATE TABLE IF NOT EXISTS pb_registry (name TEXT, UNIQUE (name) ON CONFLICT FAIL )')
    try:
        cursor.execute("INSERT INTO pb_registry VALUES (?)", (phonebook, ))
        print("{} has been created.".format(phonebook))
    except sqlite3.IntegrityError:
        print("{} already exists".format(phonebook))

def add(cursor, name, phone_number, phonebook):
    try:
        cursor.execute("INSERT INTO pb_data VALUES (?, ?, ?)", (name, phone_number, pb_id(cursor, phonebook)))
        print("Added an entry to {}\n{}\t{}".format(phonebook, name, phone_number))
    except sqlite3.IntegrityError:
        print("{} already exists in {}. Use the 'update' command.".format(name, phonebook))

def lookup(cursor, name, phonebook):
    rows = cursor.execute("SELECT name, phone_number FROM pb_data WHERE name LIKE ? and pb_id=?",
                                       ('%'+name+'%', pb_id(cursor, phonebook))).fetchall()
    if rows:
        print('\n'.join('\t'.join(row) for row in rows))
    else:
        print("Error: {} does not exist in {}".format(name, phonebook))

def reverse_lookup(cursor, phone_number, phonebook):
    name = cursor.execute("SELECT name, phone_number FROM pb_data WHERE phone_number=? AND pb_id=?",
                               (phone_number, pb_id(cursor, phonebook))).fetchone()
    if name:
        print('\t'.join(name))
    else:
        print('Error: {} does not exist in {}'.format(phone_number, phonebook))

def remove(cursor, name, phonebook):
    try:
        cursor.execute("DELETE FROM pb_data WHERE name=? AND pb_id=?", (name, pb_id(cursor, phonebook)))
        print("Removed {} from {}".format(name, phonebook))
    except sqlite3.OperationalError:
        return "Error: {} does not exist in {}".format(name, phonebook)

def update(cursor, name, new_phone, phonebook):
    old_phone = cursor.execute("SELECT phone_number FROM pb_data WHERE name=? AND pb_id=? LIMIT 1",
                               (name, pb_id(cursor, phonebook))).fetchone()[0]
    if old_phone:
        cursor.execute("UPDATE pb_data SET phone_number=? where name=? and pb_id=?",
            (new_phone, name, pb_id(cursor, phonebook)))
        print("Updated an entry for {} in {}.\nOld phone #: {}\tNew phone #: {}".format(
            name, phonebook, old_phone, new_phone))
    else:
        print("Error: {} does not exist in {}".format(name, phonebook))

if __name__ == '__main__':
    #parse arguments
    args = sys.argv[1:]
    command = args.pop(0)
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

    db_conn.commit()
    db_conn.close()