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
    mc.columnLayout( adjustableColumn=True )

    # default rgb color buttons
    red = mc.button( bgc=(1, 0, 0) )
    green = mc.button( bgc=(0, 1, 0) )
    blue = mc.button( bgc=(0, 0, 1) )

    # Custom colors and palettes

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