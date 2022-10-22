from fileinput import filename
import os
import time
import stat

class parent:
    def __init__(self,name,path):
        self.name=name
        self.path=os.path.join(path,self.name)
        self.id:int    

    def id(self):
        return ''.join(e for e in self.name if e.isalnum())
    
    def setName(self,newName):
        self.name=newName
    def getAbsolutePath(self):
        index=self.path.rfind('/')
        return self.path[:index]

    def getName(self):
        return self.name

    def getPath(self):
        """returns path to file/directory"""
        return self.path

    def Lastmodified(self):
        """returns details on last modification of file/directory"""
        return time.ctime(os.stat (self.path) [ stat.ST_MTIME ] )
    
    def setPath(self, newPath):
        self.path = newPath 

    def getSize(self):
        """returns size of file/directory"""
        try:
            return os.stat(self.path).st_size
        except:
            return 'file does not exist'

  