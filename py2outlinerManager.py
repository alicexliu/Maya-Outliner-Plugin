import sys
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as OpenMayaUI

def maya_useNewAPI():
    pass


# command
class Py2HelloWorldCmd(om.MPxCommand):
    kPluginCmdName = "py2outlinerManager"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return Py2HelloWorldCmd()

    def doIt(self, args):
        print ("Hello World!")


def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
            Py2HelloWorldCmd.kPluginCmdName,
            Py2HelloWorldCmd.cmdCreator
        )
    except Exception as e:
        sys.stderr.write(f"Failed to register command: {Py2HelloWorldCmd.kPluginCmdName}\n")
        raise e


def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(Py2HelloWorldCmd.kPluginCmdName)
    except Exception as e:
        sys.stderr.write(f"Failed to unregister command: {Py2HelloWorldCmd.kPluginCmdName}\n")
        raise e