
""" synopis:

    Under projectPath create:
    +-- projectName
       +---css
       +---img
       +---js

    In the projectName folder
    - create a markup names projectName.vb.ascx
    In the projectName folder
    - create a a code behind file callled projectName.vb

    In the projectName/js folder
    - create app.js

    In the projectName/css folder
    - create app.css

    At each step of the creation, verify the folder or file
    does not exist then create.  If there is a fail, raise and quit.
    (you will have to manually rollback. I don't feel like doing it
    for you.)

    Outstanding issues:
    1. assumed Tbaytel_Desktop
    2. leaves transferFront/Back code in the ASCX file
    3. is not fault tolerant.

    You can make this executable.
    Create a setup.py file:
    
       from distutils.core import setup
       import py2exe

       setup(console=['gogoboots.py'])

    and build:

       python setup.py py2exe
    
"""

import os
import errno
import time

def createDirectory(dpath):
    print "Creating Directory: "+ dpath
    try:
        os.makedirs(dpath)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    print "Success."

def createFile(fullfilename):
    print "Creating File: "+fullfilename
    try:
        open(fullfilename,'a').close()
    except:
        raise
    print "Success"
    
def createDirectoryStructure(projectPath,projectName):
    createDirectory(projectPath+"/"+projectName)
    createDirectory(projectPath+"/"+projectName + "/" + "js")
    createDirectory(projectPath+"/"+projectName + "/" + "css")
    createDirectory(projectPath+"/"+projectName + "/" + "img")
    
def createAppJS(projectPath,projectName):
    createFile(projectPath+"/"+projectName+"/js/app.js")
    with open(projectPath+"/"+projectName+"/js/app.js","w") as jsFile:
       jsFile.write("""

// javascript for """ + projectName + """ goes here.
       
       """)
       
       jsFile.write("""

function transferToBackEnd() {
    $(dotnet.example).val($('#example').val());
}
function transferToFrontEnd() {
    $('#example').val($(dotnet.example).val());
}
$(document).ready(function () {
    transferToFrontEnd();
    $('#submit').click(function () {
    transferToBackEnd(); 
    $(dotnet.submitButton).click();
        return false;
    });
});
       """)
       jsFile.close()
    

def createAppCSS(projectPath,projectName):
    createFile(projectPath+"/"+projectName+"/css/app.css")
    with open(projectPath+"/"+projectName+"/css/app.css","w") as jsFile:
        jsFile.write("""
/* Comments for application """+projectName+""" go here */

 .abc-wrapper
 {
     min-width:500px;
     min-height:500px;
     margin: 5px 5px 5px 5px; /* TRBL */
     padding:5px 5px 5px 5px; /* TRBL */
     border: 1px solid black;
 }
 
 .abc-main
 {
 }
 .abc-buttons
 {
     display:block;
     padding:20px 5px 5px 5px; /* TRBL */
 }
 .abc-left-buttons
 {
 }
 
 .abc-right-buttons
 {
 }
 .abc-input
 {
     
 }
 .abc-input label
 {
     display:inline-block;
     min-width:100px;
     font-weight:bold;
 }
 .abc-input input
 {
     min-width:100px;
 }

     """)

def createMarkup(projectPath,projectName):
    vbfile = projectName+".ascx.vb"
    classname = "DesktopModules_TbayTel_" + projectName + "_"+projectName
    createFile(projectPath+"/"+projectName+"/"+projectName+".ascx")
    controlstr = "<%@ Control Language=\"VB\" AutoEventWireup=\"false\" CodeFile=\""+vbfile+"\" Inherits=\""+classname+"\" %>"
    print "Using: " + controlstr
    print "You may want to customize this."
    dnntag= "<%@ Register TagPrefix=\"dnn\" Namespace=\"DotNetNuke.Web.Client.ClientResourceManagement\" Assembly=\"DotNetNuke.Web.Client\" %>"
    with open(projectPath+"/"+projectName+"/"+projectName+".ascx","w") as jsFile:
        jsFile.write(controlstr+
"""
"""+dnntag + """

<%--/*
    * Program: """+projectName+""" main markup
    * Author: -------------
    * Date: """+time.strftime("%c")+"""
    * Depends on: 
    * Depended on: 
    * Notes:
    *       <none>
    * Revisions:
    *       <none>
    * 
    */--%>
 

<dnn:DnnCssInclude ID="DnnAPPCSS"
       runat="server" 
       FilePath="~/DesktopModules/Tbaytel/""" + projectName+"""/css/app.css" 
       ForceProvider="DnnFormBottomProvider" 
       Priority="102" />

<dnn:DnnJsInclude ID="DnnAppSessionInclude" 
        runat="server" 
        FilePath="~/DesktopModules/Tbaytel/"""+projectName +"""/js/app.js" 
        ForceProvider="DnnFormBottomProvider" 
        Priority="230" />

        
<div class="abc-wrapper">
    <div class="abc-main">
        <div class="abc-input">
            <label for="example">Example</label>
            <input id="example" />
        </div>
    </div>
    <div class="abc-buttons">
       <div class="abc-left-buttons">
          <input type="button" id="submit" value="Submit" />
       </div>
       <div class="abc-right-buttons"></div>
       <div class="hidden">
           <asp:Button ID="btnSubmit" runat="server" />
           <asp:HiddenField ID="hdnExample" runat="server" />
       </div>
    </div>       
</div>
       
<script>       
var dotnet = (function() {
  return {
    submitButton : '#<%=btnSubmit.ClientID%>',
    example      : '#<%=hdnExample.ClientID%>'
  };
})();


</script>
"""
        )
        jsFile.close()
        
                     

def createCodeBehind(projectPath,projectName):
    createFile(projectPath+"/"+projectName+"/"+projectName+".ascx.vb")
    with open(projectPath+"/"+projectName+"/"+projectName+".ascx.vb","w") as jsFile:
        jsFile.write("""
'/*
   ' * Program: """+projectName+""" server side
   ' * Author: 
   ' * Date: """+time.strftime("%c")+"""
   ' * Depends on: 
   ' * Depended on: 
   ' * Notes:
   ' *       <none>
   ' * Revisions:
   ' *       <none>
   ' * 
   ' */
   
Partial Class DesktopModules_TbayTel_"""+projectName+"""_"""+projectName+"""
        Inherits DotNetNuke.Entities.Modules.PortalModuleBase
                '' put some code here.
End Class

        """)

def main():
    #get inputs
    print "This will create dirs and files for a simple (non-angular) app."
    print "(If they are already there, this will reset everything to a basic"
    print "template - and it will not warn you.)"
    print ""
    print "Enter full path, e.g.) b:/website/dnn_tbaytel_net/DesktopModules/Tbaytel"
    projectPath = raw_input("Enter Pathname: ")
    print "Enter application name, no extensions. e.g.) TestApp"
    projectName = raw_input("Enter Project Name: ")
    print "Would create " + projectName+ " in folder " + projectPath
    gogo = raw_input("Enter yes to continue: ")
    if gogo == "yes":
        createDirectoryStructure(projectPath,projectName)
        createMarkup(projectPath,projectName)
        createCodeBehind(projectPath,projectName)
        createAppJS(projectPath,projectName)
        createAppCSS(projectPath,projectName)

main()

    
    
