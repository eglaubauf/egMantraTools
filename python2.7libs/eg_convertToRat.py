#####################################
#LICENSE                            #
#####################################
#
# Copyright (C) 2019  Elmar Glaubauf
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
This script converts imported textures in Houdini to .rat File Format.

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""

import hou
import os
import shutil

########CONFIG ME HERE ###########

extension = ".rat"

############END CONFIG ############


def run():
    
    nodes = hou.selectedNodes()

    c = Converter(nodes)
    #Print Result
    c.finish()

############################


#HelperClass
class Entry:
    texPath = ""
    node = ""
    parm = ""

    def __init__(self, path, node, parm):
        self.texPath = path
        self.node = node
        self.parm = parm

#Converter Class
class Converter():

    def __init__(self, nodes):
        self.textures = []
        self.errors = []
        self.count = 0
        self.nodes = nodes

        #Convert stuff
        self.gatherTextures()
        self.convertFiles()
        
        return
    
    #Returns Count
    def getCount(self):
        return self.count

    #Gathers Textures to be changed
    def gatherTextures(self):
        
        for n in self.nodes:
            if n.type().name() == "texture::2.0" or n.type().name() == "principledshader::2.0" or n.type().name() == "displacetexture" :
                for p in n.parms():
                    if p.parmTemplate().type() == hou.parmTemplateType.String:
                        # Get Parm as String
                        s = p.evalAsString()
                        occur = s.rfind("/")
                        #Filter out non Files - go to next if none
                        if occur == -1:
                            continue
                        if s.startswith(hou.getenv("HSITE")):   #Leave if already in place
                            continue
                        if not os.path.exists(s):
                            #global errors
                            s = (s + " does not exist \n")
                            self.errors.append(s)
                            continue

                        #Append string to Converted List
                        if not s.endswith('.rat'):
                            self.textures.append(Entry(s, n, p))

            if n.type().name() == "materialbuilder":
                #Create a new Instance of this Class for SubChildren
                ch = Converter(n.children())
                self.count += ch.getCount()


    #Converts Files
    def convertFiles(self):
        
        cop = hou.node("/img")
        img = cop.createNode("img", "tmp")
        
        read = img.createNode("file")
        rop = img.createNode("rop_comp")
        rop.setInput(0,read,0)
        rop.parm("trange").set(0)

        #Convert Stuff
        for f in self.textures:
            filename = f.texPath
            read.parm("filename1").set(filename)
            
            #Change Filename
            namePos = filename.rfind(".")
            name = filename[:namePos]
            name += extension

            #Render
            rop.parm("copoutput").set(name)
            rop.parm("execute").pressButton()
            
            #Change Original Material/Texture
            f.node.parm(f.parm.name()).set(name)

            self.count += 1

        #Cleanup 
        img.destroy()

    #Cleanup after Converting
    def finish(self):
        text = str(self.count) + " Textures converted. \n "
        
        if errors: 
            text = self.printErrors(text)
        hou.ui.displayMessage(text)

    #Print Errors if happend - no exception to continue other files
    def printErrors(text):

        text = text + "Errors: \n"
        msg = ""
        for s in errors:
            msg = msg + s + "\n"

        text = text + msg
        return text
