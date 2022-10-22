from flask_login import UserMixin

class user(UserMixin):
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def get_username(self):
        '''returns username of the user'''
        return self.username

    def get_password(self):
        '''returns password of the user'''
        return self.password

    def get_id(self):
        '''returns the id assigned to the user'''
        return self.username