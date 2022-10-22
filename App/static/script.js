
    nameLimit();
    updateCurrentPath();
    fileNfolderCount();
    var changes='';
    const exts=['mp3','mp4','jpeg','jpg','png','pgm', 'pdf','html', 'ico'];
    const icons={'mp3':'audiotrack','mp4':'movie'}
    const img_types=['jpeg','jpg','png','pgm']
    const doc_types=['doc','odt','txt','xml','pdf','html']
    const audio_types=['mp3','ogg','wav','fav']
    const code_types=['py','cpp','js','java']
    addIcons();

    //upload button
    $("input[name='files[]']").change(function() {
        $(this).closest("form").submit();
    });
    $('.mess').each(function(){
     
        $('#show-messages').click()
    })
    function error(){
    // Get the snackbar DIV
    var x = document.querySelector(".mess")

    // Add the "show" class to DIV
    x.className = "show";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
    }

    //drag and drop upload
    Dropzone.options.myGreatDropzone = {
        // camelized version of the `id`
        paramName: "files[]", // The name that will be used to transfer the file
        maxFilesize: 100000, // MB
        maxThumbnailFilesize: 30,
        parallelUploads: 10,
        timeout: 0,
        

        // refresh the page after completing upload
        init: function() {
		    this.on('success', function(){
			    if (this.getQueuedFiles().length == 0 && this.getUploadingFiles().length == 0) {
     				loader(location);
		    	}
                
                // removes file thumbnail after upload
                $('.dropzone')[0].dropzone.files.forEach(function(file) { 
                file.previewElement.remove(); 
                });

                $('.dropzone').removeClass('dz-started');

            });
	    }
      };
    
      function updateCurrentPath(){
        
        iconright = '<i class="material-icons">arrow_forward_ios</i>'
        icondots = '<i class="material-icons">more_horiz</i>'

    }
    // adds corresponding icons to files
    function addIcons(){
        $('.file-icon').each(function(){
        var ext=($(this).attr('ext')).toLowerCase();
        if (img_types.includes(ext)){
            this.innerHTML='image'
        }
        else if(audio_types.includes(ext)){
            this.innerHTML='audiotrack'
        }
        else{
            this.innerHTML='text_snippet'
        }
        
        })
    }
    
    //context menu
    $(function() {
        $.contextMenu({
            selector: '.filee',
            callback: function(key, options) {
                const name=$(this).attr('name');            
                if (getSelected().length>1 && !($(this).hasClass('highlight')))
                {
                    uncheck();
                    highlight(name);
                }
                else if (!($(this).hasClass('highlight'))){
                    highlight(name)
                }
    
                if (key=='/changeDir'){
                    uncheck()
                    highlight(name)
                    if ($(this).attr('class').split(' ')[0]=='dir'){
                        const value=($('#bck').attr('value'))+'-'+name
                        $('#bck').attr('value',value)
                        loader(key+'/'+name)
                    }
                    else{
                        var filename=$(this).attr('value');
                        
                        openFile(filename)
                        
                    }
                }
                else if (key=='/rename'){
                    uncheck()
                    highlight(name);
                    rename($(this).attr('value'))
                }
                else if (key=='/download'){
                    $('#download').click()
                }
                else if (key=='/delete'){
                    $('#delete').modal()
                }
                else if (key=='/move'){
                  
                    moving($(this).attr('path'))
                }
                
            },
            items: {
                "/changeDir": {name: "Open"},
                "/rename": {name: "Rename"},
                "/download": {name: "Download"},
                "/delete": {name: "Delete"},
                "/move":{name:"Move"},
                "sep1": "---------",
                "quit": {name: "Quit"}
            }
        });

            
    });
    function openFile(filename){
        var ind =filename.lastIndexOf('.');
        var ext=filename.slice(ind+1);
        if (exts.includes(ext)){
            view(filename)
        }
        else{
            textEditor('/openFile/'+filename);

        }
    }

    async function logout(){
        try{
            let response = await fetch('/logout');
            let data = await response.text();
            $('html').innerHTML=data          
        } catch(error){
                console.log(error)
            }
    }
    async function textEditor(url){
        //hides addFolder and upload button on nav bar and shows save button
        $('#addFolder-nav').attr('hidden',true)
        $('#upload-nav').attr('hidden',true)
        $('#save-nav').attr('hidden',false)
        
        try{
            let response = await fetch(url);
            let data = await response.text();
            var ind=url.lastIndexOf('/')
            if (url.endsWith('.csv')){
                csv_obj=JSON.parse(data)
                var name=url.slice(ind+1)
                csvTable(csv_obj,name)
            }
            else{
                var myTextarea=document.getElementById('FileID')
                document.getElementById('FileID').innerHTML='<span id="cls" class="border border-bottom-0 border-dark" style="postion:absolute;background-color:#f7f7f7; padding:20px">'+url.slice(ind+1)+'<a onclick="closeFile()" style="padding:5px;color:black">x</a></span>'    
                var myCodeMirror = CodeMirror(myTextarea, {
                mode:  "python",
                lineNumbers: true,
                scrollbarStyle: "null"
                });
                myCodeMirror.setValue(data)
                myCodeMirror.on('change',function(data){
                    // updates 
                    changes=[data.getValue(),url.slice(ind+1)]
                    
                })
                myCodeMirror.setSize('1500','1700');
            }
            
            } catch(error){
                console.log(error)
            }
            
            
        }
        function csvTable(csv_obj,name){
          
            var table='<span id="cls" class="border border-bottom-0 border-dark" style="postion:absolute;background-color:#f7f7f7; padding:10px;">'+name+'<a onclick="closeFile()" style="padding:5px;color:black">x</a></span><br>'
            var count=0;
                table+='<table id="csv-table" class="table table-bordered" style="margin-top:7.5px">\n'
                $.each(csv_obj,function(){
                table+='<tr contenteditable>\n'
                $.each(this,function(){
                    if (count==0){
                    table+='<th> '+this+' </th>\n'  
                    }
                    else{
                        table+='<td contenteditable style="border: 0.05rem solid rgba(197, 197, 197, 0.486);font-size: 1.4rem;height: 2.5rem;border-spacing: 0rem;"> '+this+' </td>\n'
                    }
                })
                table+='</tr>\n'
                count++
                
                })
                table+=' </table>'
                $('.filess').empty()
                document.getElementById('FileID').innerHTML
                $('.filess').append(table)
                let parser = new DOMParser();
                var doc = parser.parseFromString(document.getElementById('FileID').innerHTML, 'text/html');
                document.getElementById("csv-table").addEventListener("input", function() {
                    changes=[tableToCSV(document.getElementById('csv-table')),name]
                }, false);

        }
        //give html table converts it to csv format 
        function tableToCSV(table) {
            //stores csv content
            var data = [];
            var rows = table.getElementsByTagName('tr');//csv rows
            for (var i = 0; i < rows.length; i++) {
                //column data
                var cols = rows[i].querySelectorAll('td,th');
                // store each row data
                var row = [];
                for (var j = 0; j < cols.length; j++) {
                        row.push(cols[j].innerHTML); 
                }

                data.push(row.join(","));
            }
            data = data.join('\n');
        
            return data  
        }
        //closes file
        function closeFile(){
            //if changes exists prompt user to save or discard changes and then closes file
            if (changes.length>0){
                $('#save').modal();
            }
            else{
            loader('/changeDir/'+$('#back').attr('value'))
            }
        }     
        //saves file if changes exists
        function save(){
            if (changes.length>0){
                $.post("/saveFile/"+changes[1], {"myData": changes[0]})
                changes=[]
            }
            $('#save').modal('hide')
            
        }   
    

  
    async function moving(path){
        //list possible directories to move to
        $('#listDir').empty()
        $('#Move').modal()
        if (path==undefined){
            path=$(event.target).attr('name')
        }
        if (path=='MyFiles'){
            $('#bck').css('color','#ffffff')
        }
        else{
            $('#bck').css('color','#606060')
        }
        $('#bck').attr('value',path)
        $('#moveTO').attr('value',path)
        try{
            let response = await fetch('/moveTo/'+path);
                    let data = await response.text();
                    var dirs=JSON.parse(data)
                    if (!dirs[0]){
                        $('#listDir').append('<div style="text-align:center;padding:20px"><span>This folder is empty</span></div>')
                    }
                    $.each(dirs,function(){
                    var pth=path+'-'+this
                    var name=($("#moveTo").attr('value'))
                    document.getElementById('destination').innerHTML='Move destination: '+name.slice(name.lastIndexOf('-')+1)
                    if ( !getSelected().includes(pth)){
                        var item='<tr onclick="moveTo(this)" name='+pth+' ondblclick="moving()"><td  name='+pth+'><span><i class="fa fa-folder" style="color:#606060"></i><a ondblclick="moving()" name='+pth+' style="text-decoration:none;color:black;font-size:15px" > '+this+'</a></span></td><br></tr>'
                        
                    }
                    else{
                        var item='<tr style="pointer-events: none;"><td><i class="fa fa-folder" style="color:gray"></i><a style="text-decoration:none;color:gray;font-size:15px" >'+this+'</a></td><br></tr>'
                    }
                    $('#listDir').append(item)
                })
                      
            } catch(error){
                console.log(error)
            }
    }

    async function loader(urlOption) {
        changes=[]
        $('#addFolder-nav').attr('hidden',false)
        $('#upload-nav').attr('hidden',false)
        $('#save-nav').attr('hidden',true)
        if ((event!=undefined)){
            $('#bck').attr('value',$(event.target).attr('value'))
        }
        try{
            let response = await fetch(urlOption);
            let data = await response.text();
            let parser = new DOMParser();
            var doc = parser.parseFromString(data, 'text/html');  
            document.getElementById('FileID').innerHTML=doc.querySelector('#FileID').innerHTML
            nameLimit();
            addIcons();
            updateCurrentPath();
            fileNfolderCount();

        } catch(error){
                console.log(error)
        }
        uncheck()
    };
    function fileNfolderCount(){
        fileCount = 0;
        folderCount = 0;
        $('.file').each(function(){
            fileCount++;
        })
        $('.dir').each(function(){
            folderCount++;
        })
        if (fileCount==0 && folderCount==0){
            document.querySelector('.FolderCount').innerHTML = "<span style='padding:570px' >There is nothing here</span>";
            document.querySelector('.FileCount').innerHTML = "";

        }
        else{
            if (fileCount==0){
                document.querySelector('.FileCount').innerHTML = "";
            }
            if (folderCount==0){
                $('.folderGrid').attr('hidden',true)
                $('.FolderCount').attr('hidden',true)
                document.querySelector('.FolderCount').innerHTML = "";
            }
        }
    
    }

    //
    function nameLimit(){
        $('.file-name').each(function(){
            var filename=(this).innerHTML;
            if (( filename.length > 22 )){
                this.innerHTML = filename.slice(0, 20)+'...'
            }
        })
    }
    
    // move function 
    function moveTo(obj){
        var pathArr=($(obj).attr('name')).split('-')
        var size=pathArr.length
        
        if (!$(obj).hasClass("highlight")){
            document.getElementById('destination').innerHTML='Move destination: '+pathArr[size-1]
            $(obj).addClass("highlight").siblings().removeClass('highlight');
        }
        else{
            document.getElementById('destination').innerHTML='Move destination: '+pathArr[size-2]
            $(obj).removeClass("highlight")
        }
        var path = $(obj).attr('name')
 
        $("#moveTo").attr('value',path)
        $("#moveTo").prop('checked',true);

    }
    //back function for the move modal
    function back(){
        var dir=$(event.target).attr('value');
        var ind=dir.lastIndexOf('-');
        dir=dir.slice(0,ind)
        $(event.target).attr('name',dir)
        $('#moveTo').attr('value',dir)
        if (ind !=-1){
            moving()
        }     
        
    }
    // unchecks or deselects selected files/directories
    $(window).bind('beforeunload', function (e) {
        uncheck()
        if (changes.length>0){
            var dialogText = 'Do you really want to leave this site?';
            e.returnValue = dialogText;
            return dialogText;

        }
    });
    //opens delete modal
    function deleteModal(name) {
        uncheck()
        name = "#" + name
        $(name).prop("checked", true);
        $('form#myForm').submit();
        $('#delete').modal();
    }
    //closes delete modal
    function close() {
        $('#delete').modal('hide');
    }
    //opens rename modal
    function rename(name) {
        $('#src').val(name)
        $('#name').val(name)
        $('#rename').modal();
    }
    //deselects file
    function uncheck() {
        $('input[name="mycheckbox"]').each(function () {
            this.checked = false;
        });
        $('.filee').each(function () {
            $(this).removeClass('highlight')
        });
        $('#deselect-nav').attr('hidden',true)
    }
    function getSelected(){
        var selects=[]
        $('.filee').each(function(){
            if ($(this).hasClass('highlight')){
                selects.push($(this).attr('path')+'-'+$(this).attr('value'))
            }
        })
        return selects;
    }
  
    //highlights/dehighlights row on click
    function highlight(id) {
        
        var obj=$('div[name="'+id+'"')
        
        if ((obj.hasClass('highlight'))) {
            obj.removeClass("highlight");
            $("#" + id).prop("checked", false);
        }
        else {
            obj.addClass("highlight");
            $("#" + id).prop("checked", true);
        }
        var selects=getSelected().length;
        if(selects>1){
            $('#deselect-nav').attr('hidden',false)
        }
        else{
            $('#deselect-nav').attr('hidden',true)
        }
    };
    // make alert disappear automatically
    $(document).ready(function () {
        window.setTimeout(function () {
            $(".alert").delay(500).slideDown(800, function () {
                $(this).remove();
            });
        }, 5000);

    });

    // Close image viewer modal
    function closeViewModal() {
        //get value attribute of cursor element
        let cursor   = document.getElementById('cursor').getAttribute('value');

        const myTag = document.getElementById(cursor);
        let filePath = myTag.getAttribute("src").slice(2);     

        $('#otherFiles').attr("src", ''); //set value of src attribute to empty string
        $('#video').attr("src", '');
        $('#viewImg').modal('hide'); //hide viewer modal
        $.post("/closeViewer/", {"myFile": filePath});

    }


    async function view(filePath){
    
        $.post("/view/"+filePath, {"myFile": filePath})
        $('#viewImg').modal('show');
        let path = '../static/views/' + filePath
        //supported video formats
        let fileExt = ['jpg', 'png', 'pgm', 'jpeg', 'mp3', 'wav','ogg', 'pdf', 'html', 'ico','gif']
        let videoExt = ['mp4','webm', 'ogg' ]
        let index = filePath.lastIndexOf('.')
        let extension = (filePath.slice(index+1)).toLowerCase();
        console.log(extension)
        
        document.getElementById('LongTitle').innerHTML = (filePath) //set modal title to opened file name
        if (videoExt.includes(extension)){
            //hide other sources and display video
            $('#video').css('display', 'block');
            $('#otherFiles').css('display', 'none');
            $('#video').attr("src", path)
            document.getElementById('cursor').setAttribute('value',"video")

        }
        else if (fileExt.includes(extension)){
             //hide video source and display audio/image/pdf
            $('#video').css('display', 'none');
            $('#otherFiles').css('display', 'table');
            $('#otherFiles').attr("src", path) 
            document.getElementById('cursor').setAttribute('value',"otherFiles")
        }

    }