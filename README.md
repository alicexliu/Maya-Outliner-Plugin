# Maya Outliner Plugin

Description
------------
Maya outliner manager that allows users to easily color and rename objects 

Explanation of code structure
------------


Instructions to install and run the project
------------
1. Download Autodesk Maya (Free for students)
2. Set up the build environment/Maya Devkit (we used Maya 2025 Update 3 DevKit)
    * [Windows](https://help.autodesk.com/view/MAYADEV/2025/ENU/?guid=Maya_DEVHELP_Setting_up_your_build_Windows_environment_64_bit_html)
    * [Linux](https://help.autodesk.com/view/MAYADEV/2025/ENU/?guid=Maya_DEVHELP_Setting_up_your_build_Linux_environment_html)
    * [MacOS](https://help.autodesk.com/view/MAYADEV/2025/ENU/?guid=Maya_DEVHELP_Setting_up_your_build_Mac_OS_X_environment_html)
3. Load the plug-in: [Instructions](https://help.autodesk.com/view/MAYADEV/2025/ENU/?guid=Maya_DEVHELP_LoadingAndUnloadingPlugins_Loading_Samples_Plug_ins_Into_Maya_html)
4. Open the Maya Script Editor, navigate to the Python tab, and run:
```
import maya.cmds as cmds
cmds.py2OutlinerManager()
```