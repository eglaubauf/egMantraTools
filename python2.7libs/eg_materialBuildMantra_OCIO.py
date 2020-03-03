#####################################
#              LICENSE              #
#####################################
#
# Copyright (C) 2020  Elmar Glaubauf
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
This script will create a Redshift Node Network based on a file selection

Twitter: @eglaubauf
Web: www.elmar-glaubauf.at
"""

import re
import hou
import os
import shutil

def run():
    MaterialBuild()

class MaterialBuild:

    #vars
    extension = ".rat"
    #Context
    obj = hou.node("/obj")
    mat = hou.node("/mat")


    def __init__(self):

        #Init Variables
        self.initVariables()
        #Fill Variables (by User)
        self.getFiles()
        #Fill Username (by User)
        self.username = self.getName()
        #Create Material
        self.createMaterial()


    def initVariables(self):
        # Variables used by Class
        self.img = ""

        #MaterialComponents
        self.base_color = ""
        self.roughness = ""
        self.normal = ""
        self.metallic = ""
        self.reflect = ""
        self.displace = ""
        self.bump = ""
        self.ao = ""
        self.uv = ""


    def createMaterial(self):

        #Create Materialbuilder
        mb = self.mat.createNode("materialbuilder")
        mb.setName(self.username, True)
        mb.moveToGoodPosition()

        #Get Surface Output Node
        so = mb.glob("surface_output")[0]
        #Create Mantra Specific Nodes
        se = mb.createNode("surfaceexports")
        so.setInput(0, se, 0)
        so.setInput(1, se, 1)
        so.setInput(4, se, 2)

        #Create PrincipledShader
        pc = mb.createNode("principledshader")

        #Layer Export
        layer = mb.createNode("parameter")
        layer.parm("parmname").set("layer")
        layer.parm("exportparm").set(1)
        layer.parm("useownexportcontext").set(1)
        layer.parm("parmtype").set("struct")
        layer.parm("parmtypename").set("ShaderLayer")
        layer.setInput(0,pc,2)
        se.setInput(0, pc, 2)

        self.uv = mb.createNode("uvcoords::2.0")

        #################
        ######Layers#####
        #################
        if self.base_color is not "":
            self.base_color = self.convertFiles(self.base_color, 0)
            self.createTexture(mb, pc, self.base_color, "Base_Color")
            if self.ao is not "":
                self.ao = self.convertFiles(self.ao, 1)
                createTexture(mb, pc, ao, "Ambient_Occlusion")
        if self.roughness is not "":
            self.roughness = self.convertFiles(self.roughness, 1)
            self.createTexture(mb, pc, self.roughness, "Roughness")
        if self.metallic is not "":
            self.metallic = self.convertFiles(self.metallic, 1)
            self.createTexture(mb, pc, self.metallic, "Metallic")
        if self.reflect is not "":
            self.reflect = self.convertFiles(self.reflect, 1)
            self.createTexture(mb, pc, self.reflect, "Reflectivity")
        if self.normal is not "":
            self.normal = self.convertFiles(self.normal, 1)
            self.createNormal(mb, pc, self.normal, "Normal")
        if self.displace is not "":
            self.displace = self.convertFiles(self.displace, 1)
            self.createDisplace(mb, pc, self.displace,"Displace")
        if self.bump is not "":
            self.bump = self.convertFiles(self.bump, 1)
            self.createNormal(mb, pc, self.bump, "Bump")

        mb.layoutChildren()

        return

    def createTexture(self, parent, connector, channel, channelName):

        #Create Texture Object and set String
        tex = parent.createNode("texture::2.0")
        tex.setName(channelName, True)
        tex.parm("map").set(channel)

        #Connect UV Node
        tex.setInput(0, self.uv, 0)

        #Create OCIO Node
        oc = parent.createNode("ocio_transform")
        oc.parm("fromspace").set("Utility - Linear - sRGB")
        oc.parm("tospace").set("ACES - ACEScg")

        #Connect Texture-Component to Shader and OCIO Node
        if channelName is "Base_Color":
            connector.setNamedInput("basecolor", oc, 0)
            oc.setNamedInput("from", tex, 0)
        elif channelName is "Roughness":
            connector.setNamedInput("rough", oc, 0)
            oc.setNamedInput("from",tex, 0)
        elif channelName is "Metallic":
            connector.setNamedInput("metallic", oc, 0)
            oc.setNamedInput("from",tex, 0)
        elif channelName is "Reflectivity":
            connector.setNamedInput("from", oc, 0)
            oc.setNamedInput("reflect",tex, 0)
        elif channelName is "Ambient_Occlusion":
            mult = parent.createNode("multiply")
            connector.setNamedInput("basecolor", oc, 0)
            oc.setNamedInput("from", mult, 0)
            bc = parent.glob("Base_Color")[0]
            mult.setInput(0, bc, 0)
            mult.setInput(1, tex,0)
        return

    def createNormal(self, parent, connector, channel, channelName):

        #Create Displacement Node
        tex = parent.createNode("displacetexture")
        tex.setName(channelName, True)
        tex.parm("texture").set(channel)

        #Connect UV Node
        tex.setInput(2, self.uv, 0)

        #Connect Texture-Component to Shader
        if channelName is "Normal":
            tex.parm("type").set("normal")
        elif channelName is "Bump":
            tex.parm("type").set("bump")
            tex.parm("scale").set(0.01)
        connector.setNamedInput("baseN",tex, 1)

        return

    def createDisplace(self, parent, connector,  channel, channelName):

        #Create Displacement Texture Node
        tex = parent.createNode("displacetexture")
        tex.setName(channelName, True)
        tex.parm("texture").set(channel)
        tex.parm("scale").set("0.1")

        #Connect UV Node
        tex.setInput(2, self.uv, 0)

        #Connect Displacement Node
        parent.glob("displacement_output")[0].setInput(0,tex, 0)
        parent.glob("displacement_output")[0].setInput(1,tex, 1)

        #Create Properties
        prop = parent.createNode("properties")

        #Add Template Parm
        group = prop.parmTemplateGroup()
        folder = hou.FolderParmTemplate("folder", "Shading")
        folder.addParmTemplate(hou.FloatParmTemplate("vm_displacebound", "Displacement Bound", 1))
        group.append(folder)
        prop.setParmTemplateGroup(group)
        prop.parm("vm_displacebound").set(1)

        #Connect
        parent.glob("*collect")[0].setInput(2,prop,0)

        #Layer Export
        lp =parent.createNode("layerpack")
        lp.setInput(3, tex, 0)
        lp.setInput(4, tex, 1)

        #Set Layer Properties
        layer = parent.createNode("parameter")
        layer.parm("parmname").set("layer")
        layer.parm("exportparm").set(1)
        layer.parm("useownexportcontext").set(1)
        layer.parm("exportcontext").set("displace")
        layer.parm("parmtype").set("struct")
        layer.parm("parmtypename").set("shaderlayer")

        layer.setInput(0,lp, 0)

        return


    def convertFiles(self, channel, linear):

        #Get Reference to COPs Context
        cop = hou.node("/img")
        img = cop.createNode("img", "tmp")

        #Create ReadNode
        read = img.createNode("file")

        #Set ColorSpace
        if linear == 1:
            read.parm("colorspace").set("linear")
        else:
            read.parm("colorspace").set("srgb")

        #Create RopNode
        rop = img.createNode("rop_comp")
        rop.setInput(0,read,0)
        rop.parm("trange").set(0)

        #Convert Stuff
        read.parm("filename1").set(channel)

        #Change Filename
        namePos = channel.rfind(".")
        name = channel[:namePos]
        name += self.extension

        #Render
        rop.parm("copoutput").set(name)
        rop.parm("execute").pressButton()

        #Cleanup
        img.destroy()

        #Return new Filename to Caller
        return name

    def getName(self):

        #Make InputField
        username = hou.ui.readInput("Call me Names", title="Name")[1]
        if username is "":
            exit()
        #Remove Special Chars and replace them with "_"
        for k in username.split("\n"):
            username = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
        return username.replace(" ", "_")


    def getFiles(self):

        #Read Files from User
        files = hou.ui.selectFile(title="Please choose Files to create a Material from", collapse_sequences = False, multiple_select = True, file_type = hou.fileType.Image)
        if files is "":
            exit()
        strings = files.split(";")

        #Get all entries
        for i, s in enumerate(strings):
            #Remove Spaces
            s = s.rstrip(' ')
            s = s.lstrip(' ')

            #Get Name of File
            name = s.split(".")
            k = name[0].rfind("/")
            name = name[0][k+1:]

            #Check which types have been selected. Config as you need
            if "base_color" in name.lower() or "basecolor" in name.lower():
                self.base_color = s
            elif "roughness" in name.lower():
                self.roughness = s
            elif "normal" in name.lower():
                self.normal = s
            elif "metallic" in name.lower():
                self.metallic = s
            elif "reflect" in name.lower():
                self.reflect = s
            elif "height" in name.lower():
                self.displace = s
            elif "displace" in name.lower():
                self.displace = s
            elif "bump" in name.lower():
                self.bump = s
            elif "ao" in name.lower() or "ambient_occlusion" in name:
                self.ao = s

        return
