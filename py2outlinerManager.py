import sys
import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.mel as mel

def maya_useNewAPI():
    pass

def createUIWindow():
    if cmds.window('window', exists=True):
        cmds.deleteUI('window')

    # create window
    cmds.window('window', title="Outliner Manager", widthHeight=(240, 300))

    # layout
    cmds.columnLayout( adjustableColumn=True, rowSpacing=10, columnAlign="center" )

    # add UI
    # renamer
    renamer_text = cmds.text( label="Auto Renamer", align="left")
    name_field = cmds.textField( )
    rename_button = cmds.button( label="Rename Selected Objects", command=lambda *args: renameObjs(name_field) )

    cmds.separator( height=10, style='in' )

    # default colors
    dcolors_text = cmds.text( label="Default Colors", align="left" )

    # default rgb color buttons
    cmds.gridLayout(numberOfColumns=6, cellWidthHeight=(40, 40))

    default_colors = [
        (1, 0, 0),     # Red
        (1, 0.65, 0),  # Orange
        (1, 1, 0),     # Yellow
        (0, 1, 0),     # Green
        (0, 0, 1),     # Blue
        (0.77, 0.33, 1.0)  # Purple
    ]

    for color in default_colors:
        cmds.button(
            label="", 
            bgc=color, 
            command=lambda *args, col = color: setOutlinerColor(col)
        )

    cmds.setParent('..')
    cmds.separator( height=10, style='in' )

    # custom colors and palettes
    cmds.columnLayout( adjustableColumn=True )
    ccolors_text = cmds.text( label="Custom Colors/Palettes", align="left" )

    # custom color buttons (TODO: implement logic)
    cmds.gridLayout(numberOfColumns=6, cellWidthHeight=(40, 40))
    c1 = cmds.button( label="", bgc=(1, 0, 1) )
    c2 = cmds.button( label="", bgc=(1, 1, 0) )
    c3 = cmds.button( label="", bgc=(0, 1, 1) )
    c4 = cmds.button( label="", bgc=(1, 0, 0) )
    c5 = cmds.button( label="", bgc=(0, 0, 1) )
    c6 = cmds.button( label="", bgc=(0, 1, 0) )

    cmds.setParent('..')

    #cmds.colorEditor()

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
def setButtonColor(button, color):
    cmds.button(button, edit=True, bgc=color)

# set the outliner color of selected objects
def setOutlinerColor(color):
    selected_objs = cmds.ls(selection=True)

    for obj in selected_objs:
        cmds.setAttr(f"{obj}.useOutlinerColor", True)

        # Set RGB components
        cmds.setAttr(f"{obj}.outlinerColorR", color[0])
        cmds.setAttr(f"{obj}.outlinerColorG", color[1])
        cmds.setAttr(f"{obj}.outlinerColorB", color[2])

        # Refresh Attribute Editor to show change
        mel.eval(f"updateAE {obj}")

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

# initialize plug-in
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

# uninitialize plug-in
def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(Py2OutlinerManagerCmd.kPluginCmdName)
    except Exception as e:
        sys.stderr.write(f"Failed to unregister command: {Py2OutlinerManagerCmd.kPluginCmdName}\n")
        raise e