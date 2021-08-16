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
import hou
import sys
from materialBuild_Mantra import Node
from collections import Iterable

# Run from Shelf Tool
def run():
    c = mantraOGL()
    c.link_mat(True)


# Run from RightClick Menu
def run_rc(mb, channel=None):
    """Run Single Script from Shelf Menu"""
    c = mantraOGL()
    c.link_mat(True, mb)


def run_rc_channel(tex, channel=None):
    """Run Single Script from RC Menu"""
    c = mantraOGL(tex.parent())
    c.set_ogl_texture(tex, channel)


class mantraOGL():
    """Class for Holding OGL Attributes"""
    def __init__(self, material_builder=None, load_tex=True):

        self.mb = material_builder
        self.mantra_mat = None
        self.load_tex = load_tex

    def set_material(self, material):
        self.mat = material

    def link_mat(self, load_tex=False, nodes=None):
        """Link multiple from Material Context"""
        # Get Selected if started without them
        if not nodes:
            nodes = hou.selectedNodes()
        count = 0
        if isinstance(nodes, Iterable):

            for mb in nodes:
                if mb.type().name() == "geo":
                    mb = mb.parm("shop_materialpath").evalAsNode()
                if mb.type().name() == "materialbuilder":
                    ogl = mantraOGL(load_tex)
                    ogl.link(mb)
                    count += 1
        else:
            if nodes.type().name() == "geo":
                nodes = nodes.parm("shop_materialpath").evalAsNode()
            if nodes.type().name() == "materialbuilder":
                ogl = mantraOGL(load_tex)
                ogl.link(nodes)
                count += 1
        hou.ui.displayMessage("OGL Attributes for " + str(count) + " Nodes created (RSMB Nodes only)")

    def link(self, material_builder):
        self.mb = material_builder
        # Load UI Template
        Node.mantra_OGL_UI(self.mb)
        self.setup_parms()

    def setup_parms(self):
        """Setup Parameters"""
        # Get Material within new Network
        for c in self.mb.children():
            if c.type().name() == "principledshader::2.0":
                self.mantra_mat = c

        # Link Parms to mantra_material
        if self.mantra_mat:
            # Diffuse
            self.link_vparm("ogl_diff", "basecolor")
            self.link_parm("ogl_diff_intensity", "albedomult")

            # Specular
            # self.link_parm("ogl_spec", "refl_color")
            self.link_parm("ogl_rough", "rough")
            self.link_parm("ogl_metallic", "metallic")
            self.link_parm("ogl_ior", "_ior")
            self.link_parm("ogl_spec_intensity", "reflect")
            self.link_parm("ogl_reflect", "reflect")
            # Emit
            self.link_vparm("ogl_emit", "emitcolor")
            self.link_parm("ogl_emit_intensity", "emitint")

            if self.load_tex:
                self.link_textures()

    def link_textures(self):
        """Link Textures from Shader to MaterialBuilder"""
        # Link Textures
        inputs = self.mantra_mat.inputConnectors()
        for i in inputs:
            if i:
                if i[0].outputNode():
                    if i[0].inputNode().type().name() == "texture::2.0":
                        # Diffuse Texture
                        if(i[0].inputIndex() == 0):
                            self.mb.parm("ogl_tex1").set(i[0].inputNode().parm("map"), follow_parm_reference=False)
                        # Roughness Texture
                        if(i[0].inputIndex() == 7):
                            self.mb.parm("ogl_roughmap").set(i[0].inputNode().parm("map"), follow_parm_reference=False)
                            self.mb.parm("ogl_rough").set(1)
                        # Metal Texture
                        if(i[0].inputIndex() == 14):
                            self.mb.parm("ogl_metallicmap").set(i[0].inputNode().parm("map"), follow_parm_reference=False)
                        # Emit Texture
                        if(i[0].inputIndex() == 48):
                            self.mb.parm("ogl_emissionmap").set(i[0].inputNode().parm("map"), follow_parm_reference=False)

                    if i[0].inputNode().type().name() == "displacetexture":
                        # Normal Texture
                        if(i[0].inputIndex() == 49):
                            self.mb.parm("ogl_normalmap").set(i[0].inputNode().parm("texture"), follow_parm_reference=False)

    def link_vparm(self, target, source):
        """Link a single Vector Parm"""
        self.mb.parm(target + "r").set(self.mantra_mat.parm(source + "r"), follow_parm_reference=False)
        self.mb.parm(target + "g").set(self.mantra_mat.parm(source + "g"), follow_parm_reference=False)
        self.mb.parm(target + "b").set(self.mantra_mat.parm(source + "b"), follow_parm_reference=False)

    def link_parm(self, target, source):
        """Link a single Scalar Parm"""
        self.mb.parm(target).set(self.mantra_mat.parm(source), follow_parm_reference=False)

    def set_ogl_texture(self, tex, channel):
        """Link the OGL Textures - Run from RC-Menu"""
        if channel == 1:
            self.mb.parm("ogl_tex1").set(tex.parm("map"), follow_parm_reference=False)
        elif channel == 2:
            self.mb.parm("ogl_roughmap").set(tex.parm("map"), follow_parm_reference=False)
            self.mb.parm("ogl_rough").set(1)
        elif channel == 3:
            self.mb.parm("ogl_metallicmap").set(tex.parm("map"), follow_parm_reference=False)
        elif channel == 4:
            self.mb.parm("ogl_emissionmap").set(tex.parm("map"), follow_parm_reference=False)
        elif channel == 5:
            self.mb.parm("ogl_normalmap").set(tex.parm("texture"), follow_parm_reference=False)

        hou.ui.displayMessage("Texture linked")
