import sys
from maya.cmds import cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as OpenMayaUI

def maya_useNewAPI():
    pass


# command
class Py2HelloWorldCmd(om.MPxCommand):
    kPluginCmdName = "py2HelloWorld"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return Py2HelloWorldCmd()

    def doIt(self, args):
        print ("Hello World!")


# Initialize the plug-in
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
            Py2HelloWorldCmd.kPluginCmdName, Py2HelloWorldCmd.cmdCreator
        )
    except:
        sys.stderr.write(
            "Failed to register command: %s\n" % Py2HelloWorldCmd.kPluginCmdName
        )
    raise


# Uninitialize the plug-in
def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(Py2HelloWorldCmd.kPluginCmdName)
    except:
        sys.stderr.write(
            "Failed to unregister command: %s\n" % Py2HelloWorldCmd.kPluginCmdName
        )
    raise