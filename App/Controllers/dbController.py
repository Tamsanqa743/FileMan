import sqlite3
import uuid
class dbController:
    
    def __init__(self, database):
        self.db = database

    def getConnection(self):
        '''returns connection to the database'''
        connection = sqlite3.connect(self.db)
        return connection

    def create_table(self, table):
        '''creates database tables from supplied table structure'''
        try:

            connection = self.getConnection()
            cursor = connection.cursor()
            cursor.execute(table)

        except:
            print('database already exists')

    def insert(self,user):
        '''store user data into database'''
        connection = self.getConnection()
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO users (username, password, root) VALUES(?, ?, ?)''',(user.get_username(), user.get_password(), user.get_username()+str(uuid.uuid4())))
        #commit changes to database and close the connection
        connection.commit()
        connection.close()

    def delete(self, user):
        '''delete user from database'''
        connection = self.getConnection()
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM users WHERE username = (%s)''', (user.get_username()))
        #commit changes to database
        connection.commit()
        #close connection to database
        connection.close()


    def update(self, username, password, new_password = 'old password', new_email='old email', new_username = 'old username'):
        '''update user details'''

        connection = self.getConnection()
        cursor = connection.cursor()

        if new_password != 'old password':
            cursor.execute('''UPDATE users SET Password = (?)  WHERE Username = (?)''', (new_password)(password))

        if new_username != 'old username':
            cursor.execute('''UPDATE users SET Username = (?) WHERE Username = (?)''', (new_username)(username))

        if new_email != 'old_email':
            cursor.execute('''UPDATE users SET Email = (?) WHERE Username = (?)''', (new_email)(username))

        #commit changes to database
        connection.commit()
        #close connection
        connection.close()

    def getUser(self, username):
         '''retrieves user details from database and returns it as a list'''

         connection = self.getConnection()
         cursor = connection.cursor()
         cursor.execute('''SELECT * FROM users where username = (?)''',(username,))
         user = (cursor.fetchone()) # fetch user data from database
         connection.close() #close connection

        #if user was found in database, we return user data
         if user is not None:
            return list(user)
         return [] # else return empty list

    def user_exists(self,usrname):
        '''returns a boolean on check if user is in database'''
        if len(self.getUser(usrname))>0:
            return True
        return False
