import os
from turtle import update
from flask import redirect, render_template,request, session,flash, send_from_directory,flash
from config import Configuration
from flask_session import Session
import shutil


config=Configuration()
dirCon,fileCon,dbCon=config.getControllers()
dbCon.create_table(config.getTable())
app =config.getApp()
auth=config.getAuth()
Session(app)


@app.route('/home', methods=['GET', 'POST'])
def index():
    '''renders landing page with appropriate content of user'''
    if not session.get("name"):
        return redirect("/login")
    directory,files=usr_dir_con().open()
    currentDir=usr_dir_con().getCurrentDir()
    index=currentDir.rfind('/')
    currentpath=currentDir.replace(usr_dir_con().root_dir,'')
    return render_template('upload.html',files=files,directory=directory,currentDir=currentDir[index+1:] ,currentpath=(currentpath.replace('/','-'))[1:])
    
@app.route("/", methods=["POST", "GET"])
def login():
    '''renders login '''
    if request.method == "POST":
        usrname=request.form.get("name")
        password=request.form.get("password")
        if auth.login(usrname,password):
            usrCon=config.getUsrControllers()
            usrCon.create_user_directory(request.form.get("name"))
            session["name"] = (usrCon)
            print((session['name']).getCurrentDir())
            usr_dir_con().moveHere(usr_dir_con().root_dir)
            flash('Successfully login!')
            return redirect("/home")
        else:
            flash('Username/Password invalid!','error')
    return render_template("login.html")


@app.route('/signup',methods=['GET','POST'])
def signUp():
    if request.method == "POST":
        if auth.signup(request.form.get("name"),request.form.get("password")):
            flash('Account created!')
        else:    
            flash ('That username already exists. Please choose a different one.', 'error')
        return redirect("/")
    return render_template("signup.html")

def usr_dir_con():
    return session['name']

    
@app.route("/logout",methods=['POST','GET'])
def logout():
    print(session['name'])
    session["name"] = None
    return redirect("/")


@app.route('/uploader/', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file_list = request.files.getlist('files[]')
        currentDir=usr_dir_con().getCurrentDir()
        fileCon.fileUpload(file_list,currentDir)
        flash('Upload complete')
        return redirect('/home')
    
    
@app.route('/openFile/<name>')
def openFile(name):
    path=usr_dir_con().getCurrentDir()+'/'+name
    return fileCon.getContent(path)

@app.route('/saveFile/<name>',methods=['GET','POST'])
def saveChanges(name):
    path=usr_dir_con().getCurrentDir()+'/'+name
    fileCon.save(path,request.form['myData'])
    return redirect('/home')

@app.route('/delete/',methods=['GET','POST'])
def deleteFiles():
    '''deletes multiple file(s)/folder(s)'''
    if request.method == 'POST':
        for name in request.form.getlist("mycheckbox"):
            currentDir=usr_dir_con().getCurrentDir()
            if os.path.isdir(currentDir+"/"+name):
                deleteFolder(name)
            else:
                fileCon.remove(name,currentDir) 
    return redirect('/home')

@app.route('/deleteFile/<name>')
def deleteFile(name):
    '''deletes individual file'''
    currentDir=usr_dir_con().getCurrentDir()
    if os.path.isdir(currentDir+"/"+name):
        deleteFolder(name)
    else:
        fileCon.remove(name,currentDir)

    return redirect('/home')
@app.route('/deleteFolder/<foldername>',methods=['GET','POST'])
def deleteFolder(foldername):
    '''deletes individual folder'''
    usr_dir_con().remove(foldername)
    return redirect('/home')
   
@app.route('/download', methods=['GET', 'POST'])
def download_file():
    '''checks if the download is of a single file or batch files,
    downloads if mutiple files are selected '''
    if request.method == 'POST':
        currentDir=usr_dir_con().getCurrentDir()
        list=request.form.getlist("mycheckbox")
        size = len(list)
        if size > 1 :
            archive = dirCon.compress(currentDir, list)
            index = archive.rfind('/')
            archiveName = archive[index + 1:]
            return send_from_directory(currentDir, archiveName),fileCon.remove(archiveName,currentDir)
        if size == 1 :
            file = list[0]
            filePath = currentDir + '/' + file
            if os.path.isdir(filePath):
                archive = shutil.make_archive(file, 'zip',currentDir+'/'+ file)
                index = archive.rfind('/')
                return send_from_directory(archive[0:index], file+'.zip'), fileCon.remove(archive,currentDir)
            else:
                return send_from_directory(currentDir, file)

    return redirect('/home') # need to fix for download using file dropdown


@app.route('/changeDir/<name>', methods=['GET', 'POST'])
def changeDir(name):
    '''updates the currentdirectory controller'''
    if name=='MyFiles' and usr_dir_con().getCurrentDir()!=usr_dir_con().getRoot_dir():
        usr_dir_con().update(name,usr_dir_con().getRoot_dir()+'/MyFiles')
    elif (usr_dir_con().dirExists(name)):
        usr_dir_con().update(name,usr_dir_con().getCurrentDir()+'/'+name)
    return redirect('/home')

@app.route('/rename',methods=['POST','GET'])
def rename():
    ''''''
    if request.method=='POST':
        oldName=request.values.get("src")
        newName=request.form.get('newName')
        currentDir=usr_dir_con().getCurrentDir()
        path=os.path.join(currentDir,oldName)
        if oldName==newName:
            flash('No changes made','neutral')
        elif os.path.isdir(path):
            if  usr_dir_con().changeName(oldName,newName) :
                flash("'{}' renamed to '{}' ".format(oldName,newName))
            else:
                flash('Directory with that name already exists. Choose different name','error')
        else:
            if fileCon.changeName(oldName,newName,currentDir):
                flash("'{}' renamed to '{}' ".format(oldName,newName))
            else:
                flash('Directory with that name already exists. Choose different name','error')

        return redirect('/home')

@app.route('/back',methods=['GET', 'POST'])
def back():
    '''goes a directory back'''
    usr_dir_con().closeDir()
    return redirect('/home')

@app.route('/addFolder/',methods=['GET','POST'])
def addFolder():
    '''new folder creation,returns approriate message'''
    if request.method=='POST':
        created=usr_dir_con().addDir(request.form.get('folder'))
        if created:
            flash("Directory successfully created.") 
        else:
            flash('Directory with that name already exists. Choose different name',"error")
        return redirect('/home')


@app.route('/moveTo/<path>',methods=['GET', 'POST'])
def list_dir(path):
    '''lists directories inside given path'''
    path=path.replace('-','/')
    path=path.replace("'",'')
    return usr_dir_con().listDir(path)

@app.route('/move/', methods = ['GET', 'POST'])
def move():
    '''Move file to different directory'''
    files=request.form.getlist("mycheckbox")
    dest=request.form.getlist("checkbox")

    dest=usr_dir_con().root_dir+('/'+(dest[0]).replace('-','/'))
 
    for i in files:  
        src = os.path.join(usr_dir_con().getCurrentDir(),i)
        fileCon.move(src,dest)
    flash("File moved successfully.")
    return redirect('/home')
    
@app.route('/view/<filename>', methods=['GET', 'POST'])
def view(filename):
    '''prepares provided file for viewing'''
    print(filename)
    src_path = usr_dir_con().getCurrentDir() + '/' + filename
    dst_path = app.root_path + '/static/views/'+filename

    fileCon.createFileLink(src_path, dst_path)
    return 'done'

@app.route('/closeViewer/', methods=['GET', 'POST'])
def closeViewer():
    filePath = app.root_path + (request.form['myFile'])
    print(filePath, 'is to be deleted')
    fileCon.removeLink(filePath)
    return 'done'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0" ,port='15000')  # If any error, to show up on screen
