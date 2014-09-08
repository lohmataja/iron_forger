import os, sqlite3
class AlreadyExists(Exception):
    pass
class DoesNotExist(Exception):
    pass
class PhonebookHandler():
    def __init__(self):
        pass
    def __enter__(self):
        self.db_conn = sqlite3.connect('./phonebook.db')
        self.cursor = self.db_conn.cursor()

    def pb_id(self, phonebook):
        return self.cursor.execute("SELECT ROWID FROM pb_registry WHERE name=?", (phonebook, )).fetchone()[0]

    # def exists(self, entry, field, db):
    #     return self.cursor.execute("SELECT * FROM {} WHERE {}=? LIMIT 1".format(db, field), (entry, )).fetchone() != None

    def create(self, pb_name):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS pb_data (name TEXT, phone_number TEXT, pb_id INTEGER, UNIQUE (name, pb_id) ON CONFLICT FAIL )')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS pb_registry (name TEXT, UNIQUE (name) ON CONFLICT FAIL )')
        try:
            self.cursor.execute("INSERT INTO pb_registry VALUES (?)", (pb_name, ))
        except sqlite3.IntegrityError:
            raise AlreadyExists("{} already exists".format(pb_name))

    def add(self, name, phone_number, phonebook):
        try:
            self.cursor.execute("INSERT INTO pb_data VALUES (?, ?, ?)", (name, phone_number, self.pb_id(phonebook)))
        except sqlite3.IntegrityError:
            raise AlreadyExists("{} already exists in {}. Use the 'update' command.".format(name, phonebook))

    def lookup(self, entry, field, phonebook):
        row = self.cursor.execute("SELECT name, phone_number FROM pb_data WHERE {}=? and pb_id=?".format(field),
                                           (entry, self.pb_id(phonebook))).fetchone()[0]
        if row:
            return row
        else:
            raise DoesNotExist("Error: {} does not exist in {}".format(entry, phonebook))

    # def reverse_lookup(self, phone_number, phonebook):
    #     return self.cursor.execute("""SELECT name, phone_number FROM pb_data
    #           WHERE phone_number=? AND pb_id=?""", (phone_number, self.pb_id(phonebook))).fetchall()

    def remove(self, name, phonebook):

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_conn.commit()
        self.db_conn.close()