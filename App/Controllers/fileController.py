import os
import shutil
import csv
import json
class fileController:

    def __init__(self,File):
        self.file=File

    def fileUpload(self,files,currentDir):
        '''saves given file object(s) to current directory '''
        for file in files:
            target=os.path.join(currentDir,file.filename)
            file.save(target)

    def changeName(self,oldName,newName,path):
        '''Change name of current file to a new name'''
        dest=os.path.join(path,newName)
        src=os.path.join(path,oldName)
        if self.fileExists(newName, path):
            return False
        else:
            os.rename(src,dest)
            return True

    def fileExists(self,name,path):
        '''checks if a file exists '''
        path=os.path.join(path,name)
        if os.path.exists(path):
            return True
        else:
            return False

    def getContent(self,path):
        '''returns content of file given its path'''
        ind= path.rfind('.')
        if (path[ind+1:]=='csv'):
            content=[]
            with open(path, 'r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    content.append(row)
            content=json.dumps(content)
        else:
            file=open(path,'r')
            content=file.read()
            file.close()
        return content
  
    def remove(self,name,currentDir):
        '''remove a file given its name and current directory'''
        path=os.path.join(currentDir,name)
        os.remove(path)

    def removeLink(self,fullName):
        '''remove a file given its name and current directory'''
        os.remove(fullName)
        return 'done'

   
    def save(self,path,changes):
        file=open(path,'w')
        file.write(changes)
        file.close()

    
    def move(self, src, destDir):
        '''Move a file to new directory'''
        try:
            shutil.move(src, destDir)
            return True

        except:
            return False

    def createFileLink(self, src, dst):
        '''Create a link to the supplied source to the desired destination'''
        os.symlink(src, dst)
    
    
    

            
