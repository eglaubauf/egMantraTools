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
import sys
from PySide2 import QtWidgets, QtCore

import materialBuild_Mantra.core as core
import materialBuild_Mantra.view as view

# Where is this script?
# SCRIPT_LOC = os.path.split(__file__)[0]

if (sys.version_info > (3, 0)):
    import importlib
    importlib.reload(core)
    importlib.reload(view)
else:
    reload(core)
    reload(view)

'''
Open with

import materialBuild_RS.controller as matBuildRS
reload(matBuildRS)
matBuildRS.open()

'''

develop = False
tmpWindow = None


def open(develop=False):

    if develop:
        reload(core)
        reload(view)
    try:
        tmpWindow.close()
    except:
        pass

    tmpWindow = Controller()
    tmpWindow.show()


class Controller(QtWidgets.QDialog, view.Ui_RSMatBuilder):

    def __init__(self, parent=hou.qt.mainWindow()):
        super(Controller, self).__init__(parent)

        self.setupUi(self)
        self.configure_uistates()

        # Set Houdini Style to Window
        self.setProperty("houdiniStyle", True)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.core = core.Core()
        self.create_connections()

    # linking Buttons to Functions
    def create_connections(self):

        self.cbx_applyMat.toggled.connect(self.set_apply_mat)
        self.cbx_context.toggled.connect(self.set_context)

        self.cbx_convert.toggled.connect(self.set_convert)
        self.cbx_convertRat.toggled.connect(self.set_convert_rat)

        self.cbx_setupOGL.toggled.connect(self.set_ogl)
        self.cbx_useTex.toggled.connect(self.use_tex)

        self.cbx_heightDisp.toggled.connect(self.set_height_displace)
        self.cbx_ccDiffuse.toggled.connect(self.set_cc_diffuse)
        self.cbx_diffLinear.toggled.connect(self.set_diff_linear)

        self.cbx_bumpLinear.toggled.connect(self.set_bump_linear)
        self.cbx_dispLinear.toggled.connect(self.set_disp_linear)

        self.cbx_diffpt.toggled.connect(self.set_diff_pt)
        self.cbx_diffPack.toggled.connect(self.set_diff_pack)

        self.fld_username.textChanged.connect(self.set_name)




        self.buttonBox.rejected.connect(self.destroy)
        self.buttonBox.accepted.connect(self.execute)

    def configure_uistates(self):
        self.cbx_convert.setDisabled(True)
        self.cbx_heightDisp.setDisabled(True)
        self.cbx_ccDiffuse.setDisabled(True)
        self.cbx_diffLinear.setDisabled(True)
        self.cbx_convertRat.setDisabled(True)
        self.cbx_dispLinear.setDisabled(True)
        self.cbx_bumpLinear.setDisabled(True)


    def set_apply_mat(self):
        if self.cbx_applyMat.isChecked():
            self.core.set_apply_mat(True)
        else:
            self.core.set_apply_mat(False)

    def set_context(self):
        if self.cbx_context.isChecked():
            self.core.set_context(True)
        else:
            self.core.set_context(False)

    def set_ogl(self):
        if self.cbx_setupOGL.isChecked():
            self.core.set_ogl(True)
        else:
            self.core.set_ogl(False)

    def set_name(self):
        self.core.set_name(self.fld_username.text())

    def use_tex(self):
        if not self.cbx_useTex.isChecked():
            # Disable Texture Options
            self.cbx_convert.setDisabled(True)
            self.cbx_convert.setChecked(False)
            self.set_convert()

            self.cbx_heightDisp.setDisabled(True)
            self.cbx_heightDisp.setChecked(False)
            self.set_height_displace()

            self.cbx_ccDiffuse.setDisabled(True)
            self.cbx_ccDiffuse.setChecked(False)
            self.set_cc_diffuse()

            self.cbx_diffLinear.setDisabled(True)
            self.cbx_diffLinear.setChecked(False)
            self.set_diff_linear()

            self.cbx_bumpLinear.setDisabled(True)
            self.cbx_bumpLinear.setChecked(False)
            self.set_bump_linear()

            self.cbx_dispLinear.setDisabled(True)
            self.cbx_dispLinear.setChecked(False)
            self.set_disp_linear()

            self.cbx_convertRat.setDisabled(True)
            self.cbx_convertRat.setChecked(False)
            self.set_diff_linear()

        else:
            self.cbx_convert.setDisabled(False)
            self.cbx_heightDisp.setDisabled(False)
            self.cbx_ccDiffuse.setDisabled(False)
            self.cbx_diffLinear.setDisabled(False)
            self.cbx_convertRat.setDisabled(False)
            self.cbx_dispLinear.setDisabled(False)
            self.cbx_bumpLinear.setDisabled(False)

        self.core.set_use_tex(self.cbx_useTex.isChecked())

    def set_convert(self):
        if self.cbx_convert.isChecked():
            self.core.set_convert(True)
        else:
            self.core.set_convert(False)

    def set_convert_rat(self):
        if self.cbx_convertRat.isChecked():
            self.core.set_convert_rat(True)
        else:
            self.core.set_convert_rat(False)

    def set_height_displace(self):
        if self.cbx_heightDisp.isChecked():
            self.core.set_height_displace(True)
        else:
            self.core.set_height_displace(False)

    def set_cc_diffuse(self):
        if self.cbx_ccDiffuse.isChecked():
            self.core.set_cc_diffuse(True)
        else:
            self.core.set_cc_diffuse(False)

    def set_diff_linear(self):
        if self.cbx_diffLinear.isChecked():
            self.core.set_diff_linear(True)
        else:
            self.core.set_diff_linear(False)

    def set_bump_linear(self):
        if self.cbx_bumpLinear.isChecked():
            self.core.set_bump_linear(True)
        else:
            self.core.set_bump_linear(False)

    def set_disp_linear(self):
        if self.cbx_dispLinear.isChecked():
            self.core.set_disp_linear(True)
        else:
            self.core.set_disp_linear(False)

    def set_diff_pack(self):
        if self.cbx_diffPack.isChecked():
            self.core.set_diff_pack(True)
        else:
            self.core.set_diff_pack(False)

    def set_diff_pt(self):
        if self.cbx_diffpt.isChecked():
            self.core.set_diff_pt(True)
        else:
            self.core.set_diff_pt(False)

    def apply_user_settings(self):
        # Choose Textures
        if self.core.get_use_tex():
            f = hou.ui.selectFile(title="Please choose Files to create a Material from", collapse_sequences=False, image_chooser=False, multiple_select=True, file_type=hou.fileType.Image)
            self.core.set_files(f)

        # Convert Textures to OCIO
        if self.core.get_convert():
            self.core.convert_tex()
        # Convert Textures to .rat
        if self.core.get_convert_rat():
            self.core.convert_rat_tex()

    # Execute Material Creation
    def execute(self):
        self.apply_user_settings()
        self.core.create_material()
        self.destroy()
