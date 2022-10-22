from Models import Directory,File
import os, subprocess
import zipfile
import re
class directoryController:
    def __init__(self,Directory):
        self.dir_model=Directory
        self.root_dir:str

    def getRoot_dir(self):
        return self.root_dir
    def open(self):
        '''computes a list of files and directories in the current directory 
        in the current directory'''
        current_dir=self.getCurrentDir()
        list =os.listdir(current_dir)
        dir=[]
        files=[]
        for i in list:
            k=os.path.join(current_dir,i)
            if os.path.isdir(k):
                dir.append(Directory.Directory(i,current_dir))
            else:
                files.append(File.File(i,current_dir))    
        return (dir,files)

    def moveHere(self,path):
        self.currentdir_move=path

    def listDir(self,path):
        current_dir=self.root_dir+'/'+path
        self.moveHere(current_dir)
        list =os.listdir(current_dir)
        count=0
        dir={}
        for i in list:
            path=os.path.join(current_dir,i)
            if os.path.isdir(path):
                dir[count]=i
                count+=1

        return (dir)

    def create_user_directory(self,usrname):
        '''creates user directory upon account creation'''
        self.addDir(usrname)
        self.update(usrname,self.getCurrentDir()+'/'+usrname)
        self.addDir('MyFiles')
        self.root_dir=self.getCurrentDir()
        self.update('MyFiles',self.getCurrentDir()+'/'+'MyFiles')
     

    def changeName(self,oldName,newName):
        '''changes directory name'''
        current_dir=self.getCurrentDir()
        dest=os.path.join(current_dir,newName)
        src=os.path.join(current_dir,oldName)
        if self.dirExists(newName):
            return False
        else:
            os.rename(src,dest)
            return True


    
    def addDir(self,name):
        '''creates new directory given the name'''
        dir=os.path.join(self.getCurrentDir(),name)
        if self.dirExists(name):
            return False
        else:
            os.mkdir(dir)
            return True


    def dirExists(self,name):
        '''checks if a given directory exists in the current working directory'''
        current_dir=self.getCurrentDir()
        dir=os.path.join(current_dir,name)
        if os.path.exists(dir):
            return True
        else:
            return False

    def remove(self,name):
        '''deletes file in the current working directory given filename'''
        path=os.path.join(self.getCurrentDir(),name)
        try:
            os.rmdir(path)
        except:
            subprocess.run(['rm', '-dr', f'{path}'])
            

    def closeDir(self):
        '''closes current directory and goes a folder back'''
        currentPath=self.getCurrentDir()
        index=currentPath.rfind('/')
        currentDir=currentPath[index+1:]
        if currentDir!='MyFiles':
            currentPath=currentPath[:index]
            index=currentPath.rfind('/')
            name=currentPath[index+1:]
            self.update(name,currentPath)

    def getCurrentDir(self):
        '''returns current working directory'''
        return self.dir_model.getPath()

    def makeArchive(self, archiveObj, folderName, file):
        """make archive"""
        fileIndex = file.find(folderName)
        fileCurrentPath = file[fileIndex + len(folderName):] # get the folder/file's current path
        archiveObj.write(file, arcname=(fileCurrentPath)) # write file to zip abject

    def update(self,name,path):
        '''updates the current workind directory'''
        self.dir_model.setName(name)
        self.dir_model.setPath(path)
        return self.dir_model.getPath()

    def compress(self,folderName, list):
        """compress files in  list for download"""
        filePaths = []
        # traverse the current folder and obtain all files and directories in it.
        for root, folders, files in os.walk(folderName, topdown=False):
            for file in files:
                filePath = os.path.join(root, file)
                filePaths.append(filePath) # append paths to filePaths array

        index = folderName.rfind('/')
        name = folderName[index + 1:]
        archiveName =folderName +'/'+name + '.zip' # create the name of the archive
        archive = zipfile.ZipFile(archiveName, 'w') # instatiate zipFile object for creating the archives
        with archive :
            for file in filePaths:
                for item in list:
                    selectedFilePath = os.path.join(root, item) # get complete path of file in the list of selected files to be downloaded
                    if selectedFilePath == file: # check if current file path is present in array of all file paths
                        self.makeArchive(archive, folderName, file) # add file to archive
                    
                    # check if file is in another folder and selected for download
                    elif os.path.isdir(selectedFilePath) and re.search(item, file): 
                       self.makeArchive(archive, folderName, file) 
            return archiveName