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


class MantraMat():
    """Creates a Mantra-Material in the given context with a Name"""
    def __init__(self, context=hou.node("/mat"), name="MantraMaterial", files=None):

        # Variables used by Class
        self.img = ""

        # RS Material
        self.material_builder = None
        self.principled = None
        self.collect = None

        self.files = files
        self.context = context
        self.name = name

        self.diff_pt = False
        self.diff_packed = False

        self.bump_linear = False
        self.displace_linear = False

        self.cc_diffuse = False
        self.diff_linear = False

    def get_material_builder(self):
        """Returns the MaterialBuilder"""
        return self.material_builder

    def get_path(self):
        """Returns the Path to the MaterialBuilder"""
        return self.material_builder.path()

    def get_displace(self):
        """Checks if there is a Displacement applied"""
        if self.files["displace"]:
            return True
        else:
            return False

    def get_files(self):
        """Gets the Files withing the Materials as Dict"""
        return self.files

    def create_material(self, cc_diffuse=False, diff_linear=False, diff_pt=False, diff_packed=False, disp_linear=False, bump_linear=False):
        """Creates an Mantra-Material in the given context"""
        self.cc_diffuse = cc_diffuse
        self.diff_linear = diff_linear
        self.diff_pt = diff_pt
        self.diff_packed = diff_packed
        self.displace_linear = disp_linear
        self.bump_linear = bump_linear

        # Material Builder
        self.material_builder = self.context.createNode("materialbuilder")
        self.material_builder.setName(self.name, True)
        self.material_builder.moveToGoodPosition()

        # Mantra Material
        self.collect = self.material_builder.glob("output_collect")[0]
        self.surface_out = self.material_builder.glob("surface_output")[0]
        self.displace_out = self.material_builder.glob("displacement_output")[0]

        self.surface_exports = self.material_builder.createNode("surfaceexports")
        self.surface_out.setInput(0, self.surface_exports, 0)
        self.surface_out.setInput(1, self.surface_exports, 1)
        self.surface_out.setInput(4, self.surface_exports, 2)

        self.principled = self.material_builder.createNode('principledshader::2.0')
        self.principled.parm("basecolor_usePointColor").set(self.diff_pt)
        self.principled.parm("basecolor_usePackedColor").set(self.diff_packed)
        self.surface_exports.setInput(0, self.principled, 2)

        if self.files:
            self.create_layers()

        self.material_builder.layoutChildren()

    def create_layers(self):
        """Creates Layers for the MaterialNode"""
        if self.files["basecolor"]:
            diff = None
            cc = None
            if self.cc_diffuse:  # User Setting - Create ColorCorrecter
                cc = self.insertCC(self.material_builder, self.principled, "Base_Color")
                diff = self.create_texture(self.material_builder, cc, self.files["basecolor"], "Base_Color")
            else:
                diff = self.create_texture(self.material_builder, self.principled, self.files["basecolor"], "Base_Color")
            if self.diff_linear:  # User Setting - Diffuse is Linear
                diff.parm("srccolorspace").set("linear")
            if self.files["ao"]:
                if self.cc_diffuse:  # User Setting - Create ColorCorrecter
                    self.create_texture(self.material_builder, self.principled, self.files["ao"], "Ambient_Occlusion", cc)
                else:
                    self.create_texture(self.material_builder, self.principled, self.files["ao"], "Ambient_Occlusion")
        if self.files["roughness"]:
            self.create_texture(self.material_builder, self.principled, self.files["roughness"], "Roughness")
        if self.files["metallic"]:
            self.create_texture(self.material_builder, self.principled, self.files["metallic"], "Metallic")
        if self.files["reflect"]:
            self.create_texture(self.material_builder, self.principled, self.files["reflect"], "Reflectivity")
        if self.files["normal"]:
            self.create_normal(self.material_builder, self.principled, self.files["normal"], "Normal")
        if self.files["bump"]:
            self.create_bump(self.material_builder, self.principled, self.files["bump"], "Bump")
        if self.files["displace"]:
            self.create_displace(self.material_builder, self.collect, self.files["displace"], "Displacement")
            self.displaceFlag = 1

    def insertCC(self, parent, connector, channel):
        cc = self.material_builder.createNode("colorcorrection")
        connector.setNamedInput(channel, cc, 0)
        return cc

    def create_texture(self, parent, connector, channel, channelName, node_before=None):
        """Creates and connects a Texture"""
        tex = parent.createNode("texture::2.0")
        tex.setName(channelName, True)
        tex.parm("map").set(channel)

        if self.is_linear(channel):
            tex.parm("srccolorspace").set(1)

        if channelName == "Base_Color":
            # insert User Linear
            connector.setNamedInput("basecolor", tex, 0)
        elif channelName == "Roughness":
            connector.setNamedInput("rough", tex, 0)
        elif channelName == "Metallic":
            connector.setNamedInput("metallic", tex, 0)
            connector.parm("reflect").set(0.01)
        elif channelName == "Reflectivity":
            connector.setNamedInput("reflect", tex, 0)
        elif channelName == "Ambient_Occlusion":
            mult = parent.createNode("multiply")
            connector.setNamedInput("basecolor", mult, 0)
            if node_before:
                mult.setInput(0, node_before, 0)
            else:
                bc = parent.glob("Base_Color")[0]
                mult.setInput(0, bc, 0)
            mult.setInput(1, tex, 0)
        return tex

    def create_normal(self, parent, connector, channel, channelName):
        """Creates and connects a NormalMap"""
        # TODO: Check if working
        # Create Bump Node
        bump = parent.createNode("displacetexture")
        # Object Space Normal - seems to be a bug in RS for now (Object Space enables Tangent Space Normals)
        bump.parm("type").set('normal')

        # Create Tex
        # tex = parent.createNode("redshift::TextureSampler")
        # tex.setName(channelName, True)
        bump.parm("texture").set(channel)
        # tex.parm("tex0_gammaoverride").set('1')

        # Connect Things
        # bump.setInput(0, tex, 0)
        connector.setNamedInput("baseN", bump, 1)

    def create_displace(self, parent, connector, channel, channelName):
        """Creates and connects a DisplacementMap"""
        # TODO: Check if working
        # Create Displace Node
        displace = parent.createNode("displacetexture")

        # Create Tex
        displace.parm("texture").set(channel)

        # Displace Linear
        if not self.displace_linear:
            displace.parm("texcolorspace").set("auto")

        # Connect Things
        self.displace_out.setNamedInput("P", displace, 0)
        self.displace_out.setNamedInput("N", displace, 1)

    def create_bump(self, parent, connector, channel, channelName):
        """Creates and connects a BumpMap"""
        # TODO: Check if working
        # Create Bump Node
        bump = parent.createNode("displacetexture")

        # Object Space Normal - seems to be a bug in RS for now (Object Space enables Tangent Space Normals)
        bump.parm("type").set('bump')

        # Set Linear
        if not self.bump_linear:
            bump.parm("texcolorspace").set("auto")

        # Create Tex
        bump.parm("texture").set(channel)
        # Connect Things
        connector.setNamedInput("baseN", bump, 1)

    def is_linear(self, channel):
        """Check if the File is linear"""
        if channel.endswith("hdr"):
            return True
        if channel.endswith("exr"):
            return True
        return False
