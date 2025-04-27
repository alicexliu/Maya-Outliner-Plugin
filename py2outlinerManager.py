import sys
import maya.cmds as mc
import maya.api.OpenMaya as om

def maya_useNewAPI():
    pass

def createUIWindow():
    if mc.window('window', exists=True):
        mc.deleteUI('window')

    # create window
    mc.window('window', title="Outliner Manager", widthHeight=(100, 100))

    # layout
    mc.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")

    # add UI
    # renamer
    renamer_text = mc.text( label="Auto Renamer", align="left")
    name = mc.textField()
    name_field = mc.textField( name , edit=True, enterCommand=('') )

    mc.separator(height=10, style='in')

    # default colors
    # mc.columnLayout( adjustableColumn=True )
    dcolors_text = mc.text( label="Default Colors", align="left" )

    # default rgb color buttons
    mc.gridLayout(numberOfColumns=3, cellWidthHeight=(80, 40))
    red = mc.button( label="", bgc=(1, 0, 0) )
    green = mc.button( label="", bgc=(0, 1, 0) )
    blue = mc.button( label="", bgc=(0, 0, 1) )

    mc.setParent('..')
    mc.separator(height=10, style='in')

    # custom colors and palettes
    mc.columnLayout( adjustableColumn=True )
    ccolors_text = mc.text( label="Custom Colors/Palettes", align="left" )

    # custom color buttons (TODO: implement logic)
    mc.gridLayout(numberOfColumns=3, cellWidthHeight=(80, 40))
    c1 = mc.button( label="", bgc=(1, 0, 1) )
    c2 = mc.button( label="", bgc=(1, 1, 0) )
    c3 = mc.button( label="", bgc=(0, 1, 1) )
    c4 = mc.button( label="", bgc=(1, 0, 0) )
    c5 = mc.button( label="", bgc=(0, 0, 1) )
    c6 = mc.button( label="", bgc=(0, 1, 0) )

    mc.setParent('..')

    # show window
    mc.showWindow('window')

# get a button's background color
def getButtonColor(button):
    return mc.button(button, query=True, bgc=True)

# set a button's background color
def setColor(button, color):
    mc.button(button, edit=True, bgc=color)

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