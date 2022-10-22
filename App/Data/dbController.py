from multiprocessing import connection
import sqlite3

class dbController:
    
    def __init__(self, database):
        self.db = database

    @staticmethod
    def getConnection(self):
        connection = sqlite3.connect(self.db)
        ####
        return connection

    def insert(self,hash,  username, password, email):
        '''store user data into database'''
        connection = self.getConnection()
        connection.execute('''INSERT INTO users VALUES(?, ?, ?, ?)''',(hash, username, password, email))
        #commit changes to database
        connection.commit()
        connection.close()

    def delete(self, username):
        '''delete user from database'''
        connection = self.getConnection()
        connection.execute('''DELETE FROM users WHERE username = (%s)''', (username))
        #commit changes to database
        connection.commit()
        #close connection to database
        connection.close()


    def update(self, username, password, new_password = 'old password', new_email='old email', new_username = 'old username'):
        '''update user details'''

        connection = self.getConnection()

        if new_password != 'old password':
            connection.execute('''UPDATE users SET Password = (%s)  WHERE Username = (%s)''', (new_password)(password))

        if new_username != 'old username':
            connection.execute('''UPDATE users SET Username = (%s) WHERE Username = (%s)''', (new_username)(username))

        if new_email != 'old_email':
            connection.execute('''UPDATE users SET Email = (%s) WHERE Username = (%s)''', (new_email)(username))

        #commit changes to database
        connection.commit()
        #close connection
        connection.close()