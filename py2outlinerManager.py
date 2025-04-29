import sys
import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.mel as mel

current_palette_index = 0
target_button = None
num_custom_colors = 17

def maya_useNewAPI():
    pass

def showColorSelector(button=None):
    global target_button
    target_button = button
    
    if cmds.window('colorPickerWindow', exists=True):
        cmds.deleteUI('colorPickerWindow')
        
    # color picker window pop up
    cmds.window('colorPickerWindow', title="Color Selector", widthHeight=(300, 300))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    
    cmds.text(label="Select a color:")

    cmds.gridLayout(numberOfColumns=6, cellWidthHeight=(40, 40))
    
    # preset color options for easy edit
    colors = [
        (0.8, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 0.3, 0.3), 
        (1.0, 0.4, 0.0), (1.0, 0.6, 0.0), (1.0, 0.8, 0.0),
        (1.0, 1.0, 0.0), (0.8, 1.0, 0.0), (0.6, 1.0, 0.0),
        (0.0, 0.8, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.4),
        (0.0, 0.6, 1.0), (0.0, 0.4, 1.0), (0.0, 0.0, 1.0),
        (0.4, 0.0, 1.0), (0.6, 0.0, 1.0), (0.8, 0.0, 1.0),
        (0.2, 0.2, 0.2), (0.4, 0.4, 0.4), (0.6, 0.6, 0.6),
    ]
    
    for color in colors:
        cmds.button(
            label="",
            bgc=color,
            command=lambda *args, c=color: applySelectedColor(c)
        )
        
    cmds.setParent('..')
    
    # custom RGB input
    cmds.separator(height=10, style='in')
    cmds.text(label="Custom RGB values:")
    
    # sliders (rgb)
    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=5,
        columnAttach=('both', 8),
        columnAlign='left'
    )

    r_slider = cmds.floatSliderGrp(
        label="R", field=True,
        minValue=0.0, maxValue=1.0,
        fieldMinValue=0.0, fieldMaxValue=1.0,
        value=1.0,
        columnWidth=[(1, 18), (2, 40), (3, 50), (4, 120)]
    )

    g_slider = cmds.floatSliderGrp(
        label="G", field=True,
        minValue=0.0, maxValue=1.0,
        fieldMinValue=0.0, fieldMaxValue=1.0,
        value=0.0,
        columnWidth=[(1, 18), (2, 40), (3, 50), (4, 120)]
    )

    b_slider = cmds.floatSliderGrp(
        label="B", field=True,
        minValue=0.0, maxValue=1.0,
        fieldMinValue=0.0, fieldMaxValue=1.0,
        value=0.0,
        columnWidth=[(1, 18), (2, 40), (3, 50), (4, 120)]
    )

    # preview button
    cmds.frameLayout(label="Preview", collapsable=False)
    preview_button = cmds.button('colorPreview', label="", height=40, bgc=(1.0, 0.0, 0.0))
    cmds.setParent('..')
    
    # updating preview button color
    cmds.floatSliderGrp(r_slider, edit=True, 
                       changeCommand=lambda *args: updatePreview(r_slider, g_slider, b_slider))
    cmds.floatSliderGrp(g_slider, edit=True, 
                       changeCommand=lambda *args: updatePreview(r_slider, g_slider, b_slider))
    cmds.floatSliderGrp(b_slider, edit=True, 
                       changeCommand=lambda *args: updatePreview(r_slider, g_slider, b_slider))
    
    cmds.button(label="Apply Custom Color", command=lambda *args: applyCustomColor(r_slider, g_slider, b_slider))
    
    cmds.button(label="Cancel", command=lambda *args: cmds.deleteUI('colorPickerWindow'))
    
    cmds.showWindow('colorPickerWindow')

def updatePreview(r_slider, g_slider, b_slider):
    r = cmds.floatSliderGrp(r_slider, query=True, value=True)
    g = cmds.floatSliderGrp(g_slider, query=True, value=True)
    b = cmds.floatSliderGrp(b_slider, query=True, value=True)
    
    cmds.button('colorPreview', edit=True, bgc=(r, g, b))

def applyCustomColor(r_slider, g_slider, b_slider):
    r = cmds.floatSliderGrp(r_slider, query=True, value=True)
    g = cmds.floatSliderGrp(g_slider, query=True, value=True)
    b = cmds.floatSliderGrp(b_slider, query=True, value=True)
    
    applySelectedColor((r, g, b))

def applySelectedColor(color):
    global target_button, current_palette_index
    
    if cmds.window('colorPickerWindow', exists=True):
        cmds.deleteUI('colorPickerWindow')
    
    if target_button:
        if cmds.button(target_button, exists=True):
            cmds.button(target_button, edit=True, bgc=color)
    else:
        slot_button = f'customColor_{current_palette_index}'
        cmds.button(slot_button, edit=True, bgc=color)        
        current_palette_index = (current_palette_index + 1) % num_custom_colors
    
    cmds.refresh(force=True)
    saveCustomColors()
    setOutlinerColor(color)

def saveCustomColors():
    for i in range(num_custom_colors):
        button_name = f'customColor_{i}'
        if cmds.button(button_name, exists=True):
            color = cmds.button(button_name, query=True, bgc=True)
            cmds.optionVar(floatValue=(f'outlinerManager_customColorR_{i}', color[0]))
            cmds.optionVar(floatValue=(f'outlinerManager_customColorG_{i}', color[1]))
            cmds.optionVar(floatValue=(f'outlinerManager_customColorB_{i}', color[2]))

def loadCustomColors():
    for i in range(num_custom_colors):
        button_name = f'customColor_{i}'
        if cmds.button(button_name, exists=True):
            if cmds.optionVar(exists=f'outlinerManager_customColorR_{i}'):
                r = cmds.optionVar(query=f'outlinerManager_customColorR_{i}')
                g = cmds.optionVar(query=f'outlinerManager_customColorG_{i}')
                b = cmds.optionVar(query=f'outlinerManager_customColorB_{i}')
                cmds.button(button_name, edit=True, bgc=(r, g, b))


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

    for idx, color in enumerate(default_colors):
        cmds.button(
            f'defaultColor_{idx}',
            label="", 
            bgc=color, 
            command=lambda *args, col=color: setOutlinerColor(col)
        )

    cmds.setParent('..')
    cmds.separator( height=10, style='in' )

    # custom colors and palettes
    cmds.columnLayout( adjustableColumn=True )
    ccolors_text = cmds.text( label="Custom Colors/Palettes", align="left" )
    cmds.gridLayout('customColorGrid', numberOfColumns=6, cellWidthHeight=(40, 40))
    
    # custom color buttons
    cmds.button('addColorButton', label="+", command=lambda *args: showColorSelector())
    ccolors = [(0.5, 0.5, 0.5)] * num_custom_colors
    
    for i in range(num_custom_colors):
        button_name = f'customColor_{i}'
        
        cmds.button(
            button_name,
            label="", 
            bgc=ccolors[i],
            command=lambda *args, btn=button_name: setOutlinerColor(cmds.button(btn, query=True, bgc=True))
        )
        pmenu = cmds.popupMenu()
        cmds.menuItem(label="Change Color", command=lambda *args, btn=button_name: showColorSelector(btn))
    
    loadCustomColors()

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

# # get a button's background color
# def getButtonColor(button):
#     return cmds.button(button, query=True, bgc=True)

# # set a button's background color
# def setButtonColor(button, color):
#     cmds.button(button, edit=True, bgc=color)

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