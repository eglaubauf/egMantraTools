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
    """Run from Shelf Tool"""
    c = Converter()
    c.get_textures()
    c.convert_user()

    c.finish()

############################


class Converter():
    """This Class converts Textures to .rat Format - either pass a String List on creation or a dictionary via set_files()"""

    def __init__(self, textures=None):

        self.textures = textures
        self.errors = []

        self.files = {
            "basecolor": None,
            "roughness": None,
            "normal": None,
            "metallic": None,
            "reflect": None,
            "height": None,
            "displace": None,
            "bump": None,
            "ao": None
        }

        self.count = 0

    def set_files(self, files):
        """Set a Dictionary of Files to be converted. recommended for Scripting Usage"""

        if isinstance(files, dict):
            self.files = files
            return

        print("but here")
        if files == "":
            return
        strings = files.split(";")

        # Get all Entries
        for i, s in enumerate(strings):
            # Remove Spaces
            s = s.rstrip(' ')
            s = s.lstrip(' ')

            # Get Name of File
            name = s.split(".")
            k = name[0].rfind("/")
            name = name[0][k + 1:]

            # Check which types have been selected. Config as you need
            if "base_color" in name.lower() or "basecolor" in name.lower():
                self.files["basecolor"] = s
            elif "roughness" in name.lower():
                self.files["roughness"] = s
            elif "normal" in name.lower():
                self.files["normal"] = s
            elif "metallic" in name.lower():
                self.files["metallic"] = s
            elif "reflect" in name.lower():
                self.files["reflect"] = s
            elif "height" in name.lower():
                self.files["height"] = s
            elif "displace" in name.lower():
                self.files["displace"] = s
            elif "bump" in name.lower():
                self.files["bump"] = s
            elif "ao" in name.lower() or "ambient_occlusion" in name:
                self.files["ao"] = s

    def convert_files(self):
        """Converts a Dictionary of Files"""
        for key in self.files:
            if self.files[key]:
                self.files[key] = self.convert_file(self.files[key])

    def convert_user(self):
        """Converts a Texutre List passed as a List of string - recommend for use as a converter via Shelf Tool"""
        if self.textures is None:
            hou.ui.displayMessage("No valid Textures have been passed")
            return

        for n, f in enumerate(self.textures):
            self.textures[n] = self.convert_file(f)
            self.count += 1

    # Returns Count
    def get_count(self):
        """Returns a count of converted Files/Textures"""
        return self.count

    # Load Textures from User
    def get_textures(self):
        """Get Files from a use via User Interaction - Legacy Shelf Tool Usage"""
        # Read Files from User
        strings = hou.ui.selectFile(title="Please choose Files to create a Material from", collapse_sequences = False, multiple_select = True, file_type = hou.fileType.Image)
        if strings == "":
            exit()
        self.textures = strings.split(";")
        # Remove Leading spaces
        for c, s in enumerate(self.textures):
            self.textures[c] = s.lstrip(' ')

    # Converts Files
    def convert_file(self, tex):
        """Converts a single file from any texture to .rat"""
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

        return name

    def finish(self):
        """Cleanup after converting"""
        text = str(self.count) + " Textures converted. \n "

        if self.errors:
            text = self.printErrors(text)
        hou.ui.displayMessage(text)

    def get_files(self):
        """Returns files passed over in the files-Dict"""
        return self.files

    def printErrors(self, text):
        """Print Errors if happend - no exception to continue other files"""
        text = text + "Errors: \n"
        msg = ""
        for s in self.errors:
            msg = msg + s + "\n"

        text = text + msg
        return text
