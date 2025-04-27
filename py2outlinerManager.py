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

    # add UI
    # renamer
    mc.columnLayout( adjustableColumn=True )
    renamer_text = mc.text( label="Auto Renamer", align="left")
    name = mc.textField()
    name_field = mc.textField( name , edit=True, enterCommand=('') )

    # default colors
    # mc.columnLayout( adjustableColumn=True )
    dcolors_text = mc.text( label="Default Colors", align="left" )

    # default rgb color buttons
    mc.gridLayout()
    red = mc.button( label="", bgc=(1, 0, 0) )
    green = mc.button( label="", bgc=(0, 1, 0) )
    blue = mc.button( label="", bgc=(0, 0, 1) )

    # custom colors and palettes
    mc.columnLayout( adjustableColumn=True )
    ccolors_text = mc.text( label="Custom Colors/Palettes", align="left" )

    # custom color buttons (TODO: implement logic)
    mc.gridLayout()
    c1 = mc.button( label="", bgc=(1, 0, 0) )
    c2 = mc.button( label="", bgc=(0, 1, 0) )
    c3 = mc.button( label="", bgc=(0, 0, 1) )

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