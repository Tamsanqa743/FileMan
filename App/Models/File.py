from . import parent
class File(parent.parent):
    def __init__(self, name, path):
        super().__init__(name, path)
        
    def getExtension(self):
        '''gives the file extention'''
        ind=(self.getName()).rfind('.')
        return self.getName()[ind+1:]

    