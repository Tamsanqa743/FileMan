import sqlite3


try:
    connection = sqlite3.connect('user.db')
    with open('schema.sql') as schema:
        connection.executescript(schema.read())
except:
    print('datbase already exists')
