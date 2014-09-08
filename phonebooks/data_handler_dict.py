import os, pickle

class PhonebookHandler():
    def __init__(self):
        pass
    def __enter__(self):
        if os.path.exists("./phonebook.dat"):
            self.