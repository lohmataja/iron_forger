__author__ = 'Liuda'
import os, sys
import sqlite3
from data_handler import PhonebookHandler, DoesNotExist, AlreadyExists

def create(cursor, phonebook):
    try:
        print('{} created!'.format(phonebook))
    except AlreadyExists as e:
        print(e)

def add(pb, *args):
    name, phone_number, phonebook = args
    try:
        pb.add(name, phone_number, phonebook)
        print('Added {} to {}'.format(name, phonebook))
    except AlreadyExists as e:
        print(e)

def update(pb, *args):
    name, new_number, phonebook = args
    try:
        old_number = pb.lookup(name, phonebook)
        pb.replace(name, new_number, phonebook)
        print("Updated the entry in {}".format(phonebook))
        print("Old entry:", name, old_number, sep='\t')
        print("New entry:", name, new_number, sep='\t')
    except DoesNotExist as e:
        print(e)

def lookup(pb, *args):
    name, phonebook = args
    try:
        entries = pb.lookup(name, phonebook)
        for name, phone_number in entries:
            print(name, phone_number, sep='\t')
    except DoesNotExist as e:
        print(e)

def reverse_lookup(pb, *args):
    phone, phonebook = *args
    try:
        name = pb.find_phone(phone, phonebook)
        print(name, phone, sep='\t')
    except:
        print("Error: {} does not exist in {}".format(phone, phonebook))

def remove(pb, *args):
    #process arguments:
    name, phonebook = args
    try:
        pb.remove(name, phonebook)
        print("Error: {} does not exist in {}".format(name, phonebook))
    except DoesNotExist:
        pb.remove(name, phonebook)

if __name__ == '__main__':
    #parse arguments
    args = sys.argv[1:]
    command = args.pop(0)
    with PhonebookHandler() as pb:
        #dispatch the command
        dispatch = {'create':create,
                    'add':add,
                    'update':update,
                    'lookup':lookup,
                    'reverse_lookup':reverse_lookup,
                    'remove':remove}
        dispatch[command](pb, *args)