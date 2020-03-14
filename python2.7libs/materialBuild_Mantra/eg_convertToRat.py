#####################################
#             LICENSE               #
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

import hou

def run():

    c = Converter()
    c.get_textures()
    c.convert()

    c.finish()

############################


# Converter Class

class Converter():

    def __init__(self, textures=None):

        self.textures = textures
        self.errors = []
        self.count = 0

    # Check and convert
    def convert(self):
        if self.textures is None:
            hou.ui.displayMessage("No valid Textures have been passed")
            return

        for f in self.textures:
            self.convert_file(f)
            self.count += 1

    # Returns Count
    def get_count(self):
        return self.count

    # Load Textures from User
    def get_textures(self):

        # Read Files from User
        files = hou.ui.selectFile(title="Please choose Files to create a Material from", collapse_sequences = False, multiple_select = True, file_type = hou.fileType.Image)
        if files == "":
            exit()
        self.textures = files.split(";")
        # Remove Leading spaces
        for c, f in enumerate(self.textures):
            self.textures[c] = f.lstrip(' ')

    # Converts Files
    def convert_file(self, tex):

        cop = hou.node("/img")
        img = cop.createNode("img", "tmp")

        read = img.createNode("file")
        rop = img.createNode("rop_comp")
        rop.setInput(0, read, 0)
        rop.parm("trange").set(0)

        read.parm("filename1").set(tex)

        # Change Filename
        namePos = tex.rfind(".")
        name = tex[:namePos]
        name += ".rat"

        # Render
        rop.parm("copoutput").set(name)
        rop.parm("execute").pressButton()

        # Cleanup
        img.destroy()

    # Cleanup after Converting
    def finish(self):
        text = str(self.count) + " Textures converted. \n "

        if self.errors:
            text = self.printErrors(text)
        hou.ui.displayMessage(text)

    # Print Errors if happend - no exception to continue other files
    def printErrors(self, text):

        text = text + "Errors: \n"
        msg = ""
        for s in self.errors:
            msg = msg + s + "\n"

        text = text + msg
        return text
