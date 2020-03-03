#####################################
#           LICENSE                 #
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

import hou
import eg_MantraMat
import eg_setupOGL
import eg_convert
import re

reload(eg_MantraMat)
reload(eg_setupOGL)
reload(eg_convert)


class Core():

    def __init__(self):
        self.nodes = hou.selectedNodes()
        self.name = self.init_name()
        self.context = hou.node("/mat")
        self.ogl = False
        self.apply = False
        self.convert = False
        self.cc_diffuse = False
        self.diff_linear = False
        self.height_displace = False
        self.material = None
        self.useTex = False
        self.diff_pt = False
        self.diff_pack = False
        self.convert_rat = False
        self.disp_linear = False
        self.bump_linear = False

        self.files = {
            "basecolor": None,
            "roughness": None,
            "normal": None,
            "metallic": None,
            "reflect": None,
            "displace": None,
            "bump": None,
            "ao": None,
        }

    # Make Key Value Pairs for Filenames
    def set_files(self, files):

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
            elif "displace" in name.lower():
                self.files["displace"] = s
            elif "bump" in name.lower():
                self.files["bump"] = s
            elif "height" in name.lower():
                if self.height_displace:  # User sets Height as Displacement
                    self.files["displace"] = s
                else:
                    self.files["bump"] = s
            elif "ao" in name.lower() or "ambient_occlusion" in name:
                self.files["ao"] = s

    def get_files(self):
        """Returns a dictionary of Files"""
        return self.files

    def set_apply_mat(self, enabled):
        """Sets if Material gets applied """
        self.apply = enabled

    def set_context(self, enabled):
        """Sets if Material is created within the current context"""
        if enabled:
            # get Context from caller
            if self.nodes:
                self.context = self.nodes[0].parent()
            else:
                self.context = hou.node("/mat")
        else:
            self.context = hou.node("/mat")

    def set_convert(self, enabled):
        """Sets if Textures will be converted"""
        self.convert = enabled

    def set_convert_rat(self, enabled):
        """Sets if Textures will be converted to Rat"""
        self.convert_rat = enabled

    def get_convert(self):
        return self.convert

    def set_ogl(self, enabled):
        """Sets if OGL Parameters will be created"""
        self.ogl = enabled

    def set_use_tex(self, enabled):
        """Sets if Textures will be loaded"""
        self.useTex = enabled

    def set_height_displace(self, enabled):
        """Sets if Height will be loaded as Displacement"""
        self.height_displace = enabled

    def set_diff_linear(self, enabled):
        """Sets if Diffuse Textures will be loaded as Linear"""
        self.diff_linear = enabled

    def set_disp_linear(self, enabled):
        """Sets if Diffuse Textures will be loaded as Linear"""
        self.disp_linear = enabled

    def set_bump_linear(self, enabled):
        """Sets if Diffuse Textures will be loaded as Linear"""
        self.bump_linear = enabled

    def set_diff_pt(self, enabled):
        """Sets if Diffuse Color will be loaded from Point Color"""
        self.diff_pt = enabled

    def set_diff_pack(self, enabled):
        """Sets if Diffuse Color will be loaded from Packed Color"""
        self.diff_pack = enabled

    def set_cc_diffuse(self, enabled):
        """Sets if Diffuse gets a ColorCorrection Node applied"""
        self.cc_diffuse = enabled

    def get_use_tex(self):
        """Gets if Textures will be loaded"""
        return self.useTex

    def init_name(self):
        """Set the Initial Name for the Material"""
        if self.nodes:
            return self.nodes[0].name()
        else:
            return "MantraMaterial"

    def set_name(self, text):
        """Set the Name for the Material"""
        if text == "":
            if self.nodes:
                self.name = self.nodes[0].name()
                return
            else:
                self.name = "MantraMaterial"
                return
        # Check against unavailable Syntax in Houdini
        # Remove Special Chars and replace them with "_"
        for k in text.split("\n"):
            text = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
        self.name = text.replace(" ", "_")

    def get_context_name(self):
        """Get the current context"""
        return self.context.name()

    def create_material(self):
        """Creates a Mantra-Material with the context given"""
        # Create Material
        if self.get_context_name() != "mat":
            self.context = self.context.createNode("matnet")

        # Create Material
        self.material = eg_MantraMat.MantraMat(self.context, self.name, self.files)
        self.material.create_material(self.cc_diffuse, self.diff_linear, self.diff_pt, self.diff_pack, self.disp_linear, self.bump_linear)

        # Apply Material to Selection
        if self.apply:
            self.apply_mat()

        # Create OGL Attributes
        if self.ogl:
            self.create_ogl_attribs()

    def convert_tex(self):
        """Converts Textures to OCIO"""
        f = eg_convert.convertOCIO(self.files)
        f.convert()
        self.files = f.get_files()

    def create_ogl_attribs(self):
        ogl = eg_setupOGL.mantraOGL()
        ogl.link(self.material.get_material_builder())

    def apply_mat(self):
        # TODO: Replace with MANTRA Displace Settings
        displace = self.material.get_displace()
        if self.nodes:
            for n in self.nodes:
                if n.type().name() == "geo":
                    n.parm("shop_materialpath").set(self.material.get_path())
                    # if displace:
                        # n.parm("RS_objprop_rstess_enable").set(1)
                        # n.parm("RS_objprop_displace_enable").set(1)
