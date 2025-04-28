import sys
import maya.cmds as cmds
import maya.api.OpenMaya as om

def maya_useNewAPI():
    pass

def createUIWindow():
    if cmds.window('window', exists=True):
        cmds.deleteUI('window')

    # create window
    cmds.window('window', title="Outliner Manager", widthHeight=(100, 100))

    # layout
    cmds.columnLayout( adjustableColumn=True, rowSpacing=10, columnAlign="center" )

    # add UI
    # renamer
    renamer_text = cmds.text( label="Auto Renamer", align="left")
    name_field = cmds.textField( )
    rename_button = cmds.button( label="Rename Selected Objects", command=lambda *args: renameObjs(name_field) )

    cmds.separator( height=10, style='in' )

    # default colors
    # cmds.columnLayout( adjustableColumn=True )
    dcolors_text = cmds.text( label="Default Colors", align="left" )

    # default rgb color buttons
    cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(80, 40))
    red = cmds.button( label="", bgc=(1, 0, 0) )
    orange = cmds.button( label="", bgc=(1, 0.65, 0) )
    yellow = cmds.button( label="", bgc=(1, 1, 0) )
    green = cmds.button( label="", bgc=(0, 1, 0) )
    blue = cmds.button( label="", bgc=(0, 0, 1) )
    purple = cmds.button( label="", bgc=(0.5, 0, 0.5) )

    cmds.setParent('..')
    cmds.separator( height=10, style='in' )

    # custom colors and palettes
    cmds.columnLayout( adjustableColumn=True )
    ccolors_text = cmds.text( label="Custom Colors/Palettes", align="left" )

    # custom color buttons (TODO: implement logic)
    cmds.gridLayout( numberOfColumns=3, cellWidthHeight=(80, 40) )
    c1 = cmds.button( label="", bgc=(1, 0, 1) )
    c2 = cmds.button( label="", bgc=(1, 1, 0) )
    c3 = cmds.button( label="", bgc=(0, 1, 1) )
    c4 = cmds.button( label="", bgc=(1, 0, 0) )
    c5 = cmds.button( label="", bgc=(0, 0, 1) )
    c6 = cmds.button( label="", bgc=(0, 1, 0) )

    cmds.setParent('..')

    # show window
    cmds.showWindow('window')

# auto rename selected objects
def renameObjs(name_field):
    new_name = cmds.textField(name_field, query=True, text=True)
    selected_objs = cmds.ls(selection=True)

    for idx, obj in enumerate(selected_objs):
        cmds.rename(obj, f"{new_name}_{idx}")

# get a button's background color
def getButtonColor(button):
    return cmds.button(button, query=True, bgc=True)

# set a button's background color
def setColor(button, color):
    cmds.button(button, edit=True, bgc=color)

# command
class Py2OutlinerManagerCmd(om.MPxCommand):
    kPluginCmdName = "py2OutlinerManager"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return Py2OutlinerManagerCmd()

    def doIt(self, args):
        createUIWindow()

# initialize plug=in
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
            Py2OutlinerManagerCmd.kPluginCmdName,
            Py2OutlinerManagerCmd.cmdCreator
        )
    except Exception as e:
        sys.stderr.write(f"Failed to register command: {Py2OutlinerManagerCmd.kPluginCmdName}\n")
        raise e

# uninitialize plug=in
def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(Py2OutlinerManagerCmd.kPluginCmdName)
    except Exception as e:
        sys.stderr.write(f"Failed to unregister command: {Py2OutlinerManagerCmd.kPluginCmdName}\n")
        raise e