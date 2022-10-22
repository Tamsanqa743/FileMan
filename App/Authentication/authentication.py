from .user import user
from werkzeug.security import generate_password_hash, check_password_hash

class authentication:
    def __init__(self, dbcontroller) :
        self.dbcontroller = dbcontroller
   
    def return_user(self, username):
        """retrieves user from database"""
        userItem = self.dbcontroller.getUser(username)
        if userItem is None:
            return None
        else:
            return user(userItem[0], userItem[1])

    def login(self,username, password):
        """logs in user into app"""        
       
        # get user from database
        user = self.dbcontroller.getUser(username)
        if self.dbcontroller.user_exists(username):
            activeUser = self.return_user(user[0])
            if check_password_hash(activeUser.get_password(), password):
                return True                    
        return False

    def validate_username(self, username):
            """validate username provided"""
            existing_user_username = self.dbcontroller.getUser(username)
            if existing_user_username:
                return False
            return True


    def signup(self, username, password):
        '''allows new user to sign up and stores user in database'''
        hashedpw =generate_password_hash(password) #hash user password
        new_user = user(username, hashedpw)
        if  self.validate_username(username):
            self.dbcontroller.insert(new_user) #save user into database
            return True
        return False