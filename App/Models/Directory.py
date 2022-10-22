from . import parent
from . import File

class Directory(parent.parent):

    def __init__(self, name, path):
        super().__init__(name, path)
    
    def fileCount(self):
        '''returns the number of files inside a directory'''
        return 'file count'
        


   