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


class mantra_OGL_UI:

    def __init__(self, n):

        hou_parm_template_group = hou.ParmTemplateGroup()
        # Code for parameter template
        hou_parm_template = hou.StringParmTemplate("vop_compiler", "Compiler", 1, default_value=(["vcc -q $VOP_INCLUDEPATH -o $VOP_OBJECTFILE -e $VOP_ERRORFILE $VOP_SOURCEFILE"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="`findfile('scripts/vop/vopcompilermenu.cmd')`", item_generator_script_language=hou.scriptLanguage.Hscript, menu_type=hou.menuType.StringReplace)
        hou_parm_template.setTags({"sidefx::shader_isparm": "0"})
        hou_parm_template_group.append(hou_parm_template)
        # Code for parameter template
        hou_parm_template = hou.ButtonParmTemplate("vop_forcecompile", "Force Compile")
        hou_parm_template.setTags({"sidefx::shader_isparm": "0"})
        hou_parm_template_group.append(hou_parm_template)
        # Code for parameter template
        hou_parm_template = hou.FolderParmTemplate("OpenGL", "OpenGL", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
        # Code for parameter template
        hou_parm_template2 = hou.FolderParmTemplate("folder0", "Diffuse", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_diff", "Diffuse", 3, default_value=([1, 1, 1]), min=0, max=1, min_is_strict=False, max_is_strict=False, look=hou.parmLook.ColorSquare, naming_scheme=hou.parmNamingScheme.RGBA)
        hou_parm_template3.setHelp("Diffuse material color. This controls how the material reacts to diffuse lighting, by multiplying the total diffuse light cast on the material. Decreasing this value will make the material less sensitive to diffuse lighting.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_diff_intensity", "Diffuse Intensity", 1, default_value=([1]), min=0, max=2, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("The diffuse intensity multiplies the Diffuse color, allowing it to be easily adjusted without affecting the its hue or saturation.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FolderParmTemplate("ogl_numtex", "Diffuse Texture Layers", folder_type=hou.folderType.MultiparmBlock, default_value=0, ends_tab_group=False)
        hou_parm_template3.setTags({"spare_category": "OpenGL"})
        # Code for parameter template
        hou_parm_template4 = hou.ToggleParmTemplate("ogl_use_tex#", "Use Diffuse Map #", default_value=True)
        hou_parm_template4.setHelp("None")
        hou_parm_template4.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template3.addParmTemplate(hou_parm_template4)
        # Code for parameter template
        hou_parm_template4 = hou.StringParmTemplate("ogl_tex#", "Texture #", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template4.setHelp("None")
        hou_parm_template4.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
        hou_parm_template3.addParmTemplate(hou_parm_template4)
        # Code for parameter template
        hou_parm_template4 = hou.StringParmTemplate("ogl_texuvset#", "UV Set", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["uv","uv2","uv3","uv4","uv5","uv6","uv7","uv8"]), menu_labels=(["uv","uv2","uv3","uv4","uv5","uv6","uv7","uv8"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template4.setHelp("None")
        hou_parm_template4.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template3.addParmTemplate(hou_parm_template4)
        # Code for parameter template
        hou_parm_template4 = hou.StringParmTemplate("ogl_tex_min_filter#", "Minification Filter", 1, default_value=(["GL_LINEAR_MIPMAP_LINEAR"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["GL_NEAREST","GL_LINEAR","GL_NEAREST_MIPMAP_NEAREST","GL_LINEAR_MIPMAP_NEAREST","GL_NEAREST_MIPMAP_LINEAR","GL_LINEAR_MIPMAP_LINEAR"]), menu_labels=(["No filtering (very poor)","Bilinear (poor)","No filtering, Nearest Mipmap (poor)","Bilinear, Nearest Mipmap (okay)","No filtering, Blend Mipmaps (good)","Trilinear (best)"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
        hou_parm_template4.setHelp("None")
        hou_parm_template4.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template3.addParmTemplate(hou_parm_template4)
        # Code for parameter template
        hou_parm_template4 = hou.StringParmTemplate("ogl_tex_mag_filter#", "Magnification Filter", 1, default_value=(["GL_LINEAR"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["GL_NEAREST","GL_LINEAR"]), menu_labels=(["No filtering","Bilinear"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
        hou_parm_template4.setHelp("None")
        hou_parm_template4.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template3.addParmTemplate(hou_parm_template4)
        # Code for parameter template
        hou_parm_template4 = hou.StringParmTemplate("ogl_tex_wrap#", "Texture Wrap", 1, default_value=(["repeat"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["repeat","clamp","decal","mirror"]), menu_labels=(["Repeat","Streak","Decal","Mirror"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
        hou_parm_template4.setHelp("None")
        hou_parm_template4.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template3.addParmTemplate(hou_parm_template4)
        # Code for parameter template
        hou_parm_template4 = hou.StringParmTemplate("ogl_tex_vwrap#", "Texture V Wrap", 1, default_value=(["repeat"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["repeat","clamp","decal","mirror"]), menu_labels=(["Repeat","Streak","Decal","Mirror"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
        hou_parm_template4.setHelp("None")
        hou_parm_template4.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template3.addParmTemplate(hou_parm_template4)
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        hou_parm_template.addParmTemplate(hou_parm_template2)
        # Code for parameter template
        hou_parm_template2 = hou.FolderParmTemplate("folder0_1", "Specular", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_spec", "Specular", 3, default_value=([1, 1, 1]), min=0, max=1, min_is_strict=False, max_is_strict=False, look=hou.parmLook.ColorSquare, naming_scheme=hou.parmNamingScheme.RGBA)
        hou_parm_template3.setHelp("Specular material color. This controls how the material reacts to specular highlights, by multiplying specular highlights on the material. Decreasing this value will dim the material's specular highlights.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_rough", "Roughness", 1, default_value=([0.05]), min=0, max=1, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("Specular roughness. Rougher surfaces have larger but dimmer specular highlights. The valid range is 0 to 1.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_use_spec", "Enable Specular", default_value=True)
        hou_parm_template3.setHelp("Toggles contribution of the specular color. When off, no specular highlights will appear.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_metallic", "Metallic", 1, default_value=([0]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("Metallic factor, from 0-1. The more metallic a surface is (approaching 1), the less diffuse and more reflection the material will have. A metallic factor closer to zero behaves more like a dielectric material. ")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_ior", "Index of Refraction", 1, default_value=([1.33]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("Index of refraction of the material, used for fresnel calculations and reflection.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_spec_intensity", "Specular Intensity", 1, default_value=([1]), min=0, max=2, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("The specular intensity multiplies the Specular color, allowing it to be easily adjusted without affecting the its hue or saturation.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_reflect", "Reflect", 1, default_value=([0]), min=0, max=1, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("The reflectiveness of the material, from 0 (not at all reflective) to 1 (completely reflective).")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_use_reflect_map", "Use Reflect Map", default_value=True)
        hou_parm_template3.setHelp("None")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.StringParmTemplate("ogl_reflect_map", "Reflect Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template3.setHelp("Texture map which modulates the reflectiveness of the material. This is multiplied by the GL Reflect parameter for the overall reflectivity.")
        hou_parm_template3.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_reflect_map_ior", "Reflect Multiplies IOR", default_value=False)
        hou_parm_template3.setHelp("When enabled, the reflection map value is multiplied by the Index of Refraction before using IOR in lighting computations. The operation is IOR * (1+reflect), so that a value of zero in the map leaves the IOR as is, negative values decrease IOR, and positive values increase IOR.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.IntParmTemplate("ogl_reflect_map_comp", "Reflect Map Channel", 1, default_value=([0]), min=0, max=4, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=(["0","1","2","3","4"]), menu_labels=(["Luminance","Red","Green","Blue","Alpha"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_reflect_map == \\\"\\\" }")
        hou_parm_template3.setHelp("The Texture map channel from which reflectivity is selected, either the luminance of the color or one of the red, green, blue, or alpha channels.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_use_roughmap", "Use Roughness Map", default_value=True)
        hou_parm_template3.setHelp("When enabled, use the map specified in ogl_roughmap for the roughness map. If this property is not present, it is assumed to be enabled.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.StringParmTemplate("ogl_roughmap", "Roughness Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template3.setHelp("Texture map for Roughness. Rougher surfaces have larger but dimmer specular highlights. This overrides the constant ogl_rough.")
        hou_parm_template3.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_invertroughmap", "Invert Roughness Map (Glossiness)", default_value=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_roughmap == \\\"\\\" }")
        hou_parm_template3.setHelp("Invert the roughness map so that it is interpreted as a gloss map - zero is no gloss (dull), one is very glossy (shiny).")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.IntParmTemplate("ogl_roughmap_comp", "Roughness Channel", 1, default_value=([0]), min=0, max=4, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=(["0","1","2","3","4"]), menu_labels=(["Luminance","Red","Green","Blue","Alpha"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_roughmap == \\\"\\\" }")
        hou_parm_template3.setHelp("Texture component used for Roughness within the Roughness texture map, which can be the luminance of RGB, red, green, blue or alpha. This allows roughness to be sourced from packed texture maps which contain parameters in the other texture channels.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_use_metallicmap", "Use Metallic Map", default_value=True)
        hou_parm_template3.setHelp("When enabled, use the map specified in ogl_metallicmap for the metallic map. If this property is not present, it is assumed to be enabled.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.StringParmTemplate("ogl_metallicmap", "Metallic Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template3.setHelp("Texture map for Metallic. The GL Metallic parameter is multiplied by the texture map value.")
        hou_parm_template3.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.IntParmTemplate("ogl_metallicmap_comp", "Metallic Channel", 1, default_value=([0]), min=0, max=4, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=(["0","1","2","3","4"]), menu_labels=(["Luminance","Red","Green","Blue","Alpha"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_metallicmap == \\\"\\\" }")
        hou_parm_template3.setHelp("Channel of the metallic texture map to sample (luminance, red, green, blue, alpha).")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        hou_parm_template.addParmTemplate(hou_parm_template2)
        # Code for parameter template
        hou_parm_template2 = hou.FolderParmTemplate("folder0_2", "Normal", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_use_normalmap", "Use Normal Map", default_value=True)
        hou_parm_template3.setHelp("When enabled, use the map specified in ogl_normalmap for the normal map. If this property is not present, it is assumed to be enabled.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.StringParmTemplate("ogl_normalmap", "Normal Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template3.setHelp("Use a normal map to specify normals instead of interpolating normals across a polygon. The RGB values are used for the normal's XYZ vector.")
        hou_parm_template3.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.StringParmTemplate("ogl_normalmap_type", "Normal Map Type", 1, default_value=(["uvtangent"]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.Regular, menu_items=(["uvtangent","world","object"]), menu_labels=(["Tangent Space","World Space","Object Space"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal)
        hou_parm_template3.setHelp("Specifies the space that the normal map operates in: UV Tangent, World, or Object space.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.IntParmTemplate("ogl_normalbias", "Normal Map Range", 1, default_value=([0]), min=0, max=10, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=(["0","1"]), menu_labels=(["0 to 1","-1 to 1"]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_normalmap == \\\"\\\" }")
        hou_parm_template3.setHelp("The range of the normal map is either 0-1 (8b map) or -1 to 1 (floating point map). This bias must match the type of normal map used.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_normalmap_scale", "Normal Scale", 1, default_value=([1]), min=0, max=10, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_normalmap == \\\"\\\" }")
        hou_parm_template3.setHelp("Scales the X and Y components of a tangent normal map to increase or decrease the effect the normal map has on the normals.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_normalflipx", "Flip Normal Map X", default_value=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_normalmap == \\\"\\\" }")
        hou_parm_template3.setHelp("Flip the normal's X direction when applying the normal map. This may be needed for normal maps generated by other applications. ")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_normalflipy", "Flip Normal Map Y", default_value=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_normalmap == \\\"\\\" }")
        hou_parm_template3.setHelp("Flip the normal's Y direction when applying the normal map. This may be needed for normal maps generated by other applications. ")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.IntParmTemplate("ogl_normallayer", "Normal Layer", 1, default_value=([0]), min=0, max=15, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.Normal, menu_use_token=False)
        hou_parm_template3.setConditional(hou.parmCondType.DisableWhen, "{ ogl_normalmap == \\\"\\\" }")
        hou_parm_template3.setHelp("The texture layer that the UV coordinates for the normal map are sourced from.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        hou_parm_template.addParmTemplate(hou_parm_template2)
        # Code for parameter template
        hou_parm_template2 = hou.FolderParmTemplate("folder0_3", "Emission", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_emit", "Emission", 3, default_value=([0, 0, 0]), min=0, max=1, min_is_strict=False, max_is_strict=False, look=hou.parmLook.ColorSquare, naming_scheme=hou.parmNamingScheme.RGBA)
        hou_parm_template3.setHelp("Emission material color. The emission color is independent of lighting, and will appear as a constant color added to the diffuse, ambient, and specular lighting contributions.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.StringParmTemplate("ogl_emissionmap", "Emission Map", 1, default_value=([""]), naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, menu_items=([]), menu_labels=([]), icon_names=([]), item_generator_script="", item_generator_script_language=hou.scriptLanguage.Python, menu_type=hou.menuType.StringReplace)
        hou_parm_template3.setHelp("An image file used for emission texturing. Unlike a diffuse map, the emission map is not affected by lighting and appears constant. The RGB values of the emission map are multiplied by the ogl_emit color which defaults to (0,0,0), so this should be set to (1,1,1) if an emission map is used. The alpha of an emission map is ignored.")
        hou_parm_template3.setTags({"cook_dependent": "1", "filechooser_mode": "read", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.FloatParmTemplate("ogl_emit_intensity", "Emission Intensity", 1, default_value=([1]), min=0, max=2, min_is_strict=False, max_is_strict=False, look=hou.parmLook.Regular, naming_scheme=hou.parmNamingScheme.Base1)
        hou_parm_template3.setHelp("The emission intensity multiplies the Emission color, allowing it to be easily adjusted without affecting the its hue or saturation.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        # Code for parameter template
        hou_parm_template3 = hou.ToggleParmTemplate("ogl_use_emit", "Enable Emission", default_value=False)
        hou_parm_template3.setHelp("Toggles contribution of the emission color. When off, the material will not be emissive.")
        hou_parm_template3.setTags({"cook_dependent": "1", "spare_category": "OpenGL"})
        hou_parm_template2.addParmTemplate(hou_parm_template3)
        hou_parm_template.addParmTemplate(hou_parm_template2)
        hou_parm_template_group.append(hou_parm_template)
        n.setParmTemplateGroup(hou_parm_template_group)

        n.parm("ogl_numtex").set(1)
