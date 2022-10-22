import os 
from Models import Directory,File
from Controllers import directoryController,fileController,dbController
from flask import Flask 
from flask_session import Session
from Authentication.authentication import authentication
class Configuration():
    def __init__(self):
        self.currentDir=Directory.Directory("FILEMAN",os.path.expanduser('~'))
        self.currentDirCon=directoryController.directoryController(self.currentDir)
        self.currentDirCon.addDir(self.currentDir.getName())
        self.fileCon=fileController.fileController(File.File('',self.currentDirCon.getCurrentDir()))
        self.app = Flask(__name__)
        self.app.secret_key='filemanRules*!&@'
        self.app.config['UPLOAD_FOLDER'] = os.path.join("FILEMAN",os.path.expanduser('~'))
        self.app.config['SESSION_PERMANENT']= False
        self.app.config['SESSION_TYPE']= 'filesystem'
        Session(self.app)
        self.dbCon = dbController.dbController('user.db')
        self.table = """ CREATE TABLE users(
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            root TEXT NOT NULL
        );"""
        self.auth=authentication(self.dbCon)

    def getControllers(self):
        """returns controllers required by flask app"""
        return self.currentDirCon,self.fileCon, self.dbCon

    def getUsrControllers(self):
        '''returns user directory controller'''
        con=directoryController.directoryController(Directory.Directory("FILEMAN",os.path.expanduser('~')))
        print('con::::'+con.getCurrentDir())
        return con 

   
        
    def getAuth(self):
        return self.auth

    def getApp(self):
        """returns app object"""
        return self.app

    def getTable(self):
        """returns table string with columns to be created"""
        return self.table
   