import scriptcontext
import Rhino
import Rhino.ApplicationSettings.CommandAliasList as aliaslist
import Rhino.ApplicationSettings.FileSettings as filesettings
import Rhino.ApplicationSettings.EdgeAnalysisSettings as edgesettings
import Rhino.ApplicationSettings.ModelAidSettings as modelaid
import Rhino.Commands.Command as rhcommand
import Rhino.Runtime
import System.TimeSpan
import System.Windows.Forms.Screen
import datetime
import utility as rhutil


def AddAlias(alias, macro):
    """
    Adds a new command alias to Rhino. Command aliases can be added manually by
    using Rhino's Options command and modifying the contents of the Aliases tab.
    Parameters:
      alias = name of new command alias. Cannot match command names or existing
              aliases.
      macro = The macro to run when the alias is executed.
    Returns:
      True or False indicating success or failure.
    """
    return Rhino.ApplicationSettings.CommandAliasList.Add(alias, macro)


def AddSearchPath( folder, index=-1 ):
    """
    Add new path to Rhino's search path list. Search paths can be added by
    using Rhino's Options command and modifying the contents of the files tab.
    Parameters:
      folder = A valid folder, or path, to add.
      index [opt] = Zero-based position in the search path list to insert.
                    If omitted, path will be appended to the end of the
                    search path list.
    """
    return Rhino.ApplicationSettings.FileSettings.AddSearchPath(folder, index)


def AliasCount():
    "Returns number of command aliases in Rhino."
    return Rhino.ApplicationSettings.CommandAliasList.Count


def AliasMacro( alias, macro=None ):
    """
    Returns or modifies the macro of a command alias.
    Parameters:
      alias = The name of an existing command alias.
      macro [opt] = The new macro to run when the alias is executed.
    Returns:
      If a new macro is not specified, the existing macro if successful.
      If a new macro is specified, the previous macro if successful.
      None on error
    """
    rc = Rhino.ApplicationSettings.CommandAliasList.GetMacro(alias)
    if macro:
        Rhino.ApplicationSettings.CommandAliasList.SetMacro(alias, macro)
    if( rc==None ): return scriptcontext.errorhandler()
    return rc


def AliasNames():
    "Returns a list of command alias names."
    return Rhino.ApplicationSettings.CommandAliasList.Names


def AppearanceColor( item, color=None ):
    """
    Returns or modifies an application interface item's color.
    Parameters:
      item = Item number to either query or modify
             0  = View background
             1  = Major grid line
             2  = Minor grid line
             3  = X-Axis line
             4  = Y-Axis line
             5  = Selected Objects
             6  = Locked Objects
             7  = New layers
             8  = Feedback
             9  = Tracking
             10 = Crosshair
             11 = Text
             12 = Text Background
             13 = Text hover
      color[opt] = The new color value
    Returns:
      if color is not specified, the current item color
      if color is specified, the previous item color
      None if not successful
    """
    rc = None
    color = rhutil.coercecolor(color)
    appearance = Rhino.ApplicationSettings.AppearanceSettings
    grid = Rhino.ApplicationSettings.GridSettings
    if item==0:
        rc = appearance.ViewportBackgroundColor
        if color: appearance.ViewportBackgroundColor = color
    elif item==1:
        rc = grid.ThickLineColor
        if color: grid.ThickLineColor = color
    elif item==2:
        rc = grid.ThinLineColor
        if color: grid.ThinLineColor = color
    elif item==3:
        rc = grid.XAxisLineColor
        if color: grid.XAxisLineColor = color
    elif item==4:
        rc = grid.YAxisLineColor
        if color: grid.YAxisLineColor = color
    elif item==5:
        rc = appearance.SelectedObjectColor
        if color: appearance.SelectedObjectColor = color
    elif item==6:
        rc = appearance.LockedObjectColor
        if color: appearance.LockedObjectColor = color
    elif item==7:
        rc = appearance.DefaultLayerColor
        if color: appearance.DefaultLayerColor = color
    elif item==8:
        rc = appearance.FeedbackColor
        if color: appearance.FeedbackColor = color
    elif item==9:
        rc = appearance.TrackingColor
        if color: appearance.TrackingColor = color
    elif item==10:
        rc = appearance.CrosshairColor
        if color: appearance.CrosshairColor = color
    elif item==11:
        rc = appearance.CommandPromptTextColor
        if color: appearance.CommandPromptTextColor = color
    elif item==12:
        rc = appearance.CommandPromptBackgroundColor
        if color: appearance.CommandPromptBackgroundColor = color
    elif item==13:
        rc = appearance.CommandPromptHypertextColor
        if color: appearance.CommandPromptHypertextColor = color
    if( rc==None ): return scriptcontext.errorhandler()
    return rc


def AutosaveFile( filename=None ):
    """
    Returns or changes the file name used by Rhino's automatic file saving
    Parameters:
      filename [opt] = name of the new autosave file
    Returns:
      if filename is not specified, the name of the current autosave file
      if filename is specified, the name of the previous autosave file
      None on error
    """
    rc = filesettings.AutosaveFile
    if filename: filesettings.AutosaveFile = filename
    if( rc==None ): return scriptcontext.errorhandler()
    return rc


def AutosaveInterval( minutes=None ):
    """
    Returns or changes how often the document will be saved when Rhino's
    automatic file saving mechanism is enabled
    Parameters:
      minutes [opt] = the number of minutes between saves
    Returns:
      if minutes is not specified, the current interval in minutes
      if minutes is specified, the previous interval in minutes
      None on error
    """
    rc = filesettings.AutosaveInterval.TotalMinutes
    if minutes:
        filesettings.AutosaveInterval = System.TimeSpan.FromMinutes(minutes)
    if( rc==None ): return scriptcontext.errorhandler()
    return rc


def BuildDate():
    "Returns the builddate of Rhino"
    build = Rhino.RhinoApp.BuildDate
    return datetime.date(build.Year, build.Month, build.Day)


def ClearCommandHistory():
    """
    Clears contents of Rhino's command history window. You can view the
    command history window by using the CommandHistory command in Rhino.
    """
    Rhino.RhinoApp.ClearCommandHistoryWindow()


__command_serial_numbers = None

def Command(commandString, echo=True):
    """
    Runs a Rhino command script. All Rhino commands can be used in command
    scripts. The command can be a built-in Rhino command or one provided by a
    3rd party plug-in.
    Parameters:
      commandString = a Rhino command including any arguments
      echo[opt] = the command echo mode
    Returns:
      True or False indicating success or failure
    
    Write command scripts just as you would type the command sequence at the
    command line. A space or a new line acts like pressing <Enter> at the
    command line. For more information, see "Scripting" in Rhino help.

    Note, this function is designed to run one command and one command only.
    Do not combine multiple Rhino commands into a single call to this method.
      WRONG:
        rs.Command("_Line _SelLast _Invert")
      CORRECT:
        rs.Command("_Line")
        rs.Command("_SelLast")
        rs.Command("_Invert")

    Also, the exclamation point and space character ( ! ) combination used by
    button macros and batch-driven scripts to cancel the previous command is
    not valid.
      WRONG:
        rs.Command("! _Line _Pause _Pause")
      CORRECT:
        rs.Command("_Line _Pause _Pause")
    After the command script has run, you can obtain the identifiers of most
    recently created or changed object by calling LastCreatedObjects.
    """
    start = Rhino.DocObjects.RhinoObject.NextRuntimeSerialNumber
    rc = Rhino.RhinoApp.RunScript(commandString, echo)
    end = Rhino.DocObjects.RhinoObject.NextRuntimeSerialNumber
    global __command_serial_numbers
    __command_serial_numbers = None
    if( start!=end ):
        __command_serial_numbers = (start,end)
    return rc


def CommandHistory():
    "Returns the contents of Rhino's command history window"
    return Rhino.RhinoApp.CommandHistoryWindowText


def DeleteAlias( alias ):
    """
    Deletes an existing alias from Rhino.
    Parameters:
      alias = the name of an existing alias
    Returns:
      True or False indicating success
    """
    return Rhino.ApplicationSettings.CommandAliasList.Delete(alias)


def DeleteSearchPath( folder ):
    """
    Removes existing path from Rhino's search path list. Search path items can
    be removed manually by using Rhino's options command and modifying the
    contents of the files tab
    Parameters:
      folder = a folder to remove
    Returns:
      True or False indicating success
    """
    return filesettings.DeleteSearchPath(folder)


def DisplayOleAlerts( enable ):
    "Enables/disables OLE Server Busy/Not Responding dialog boxes"
    Rhino.Runtime.HostUtils.DisplayOleAlerts( enable )


def EdgeAnalysisColor( color=None ):
    """
    Returns or modifies edge analysis color displayed by the ShowEdges command
    Parameters:
      color [opt] = the new color
    Returns:
      if color is not specified, the current edge analysis color
      if color is specified, the previous edge analysis color
      None on error
    """
    rc = edgesettings.ShowEdgeColor
    if color: edgesettings.ShowEdgeColor = color
    if( rc==None ): return scriptcontext.errorhandler()
    return rc


def EdgeAnalysisMode( mode=None ):
    """
    Returns or modifies edge analysis mode displayed by the ShowEdges command
    Parameters:
      mode [opt] = the new display mode. The available modes are
                   0 - display all edges
                   1 - display naked edges
    Returns:
      if mode is not specified, the current edge analysis mode
      if mode is specified, the previous edge analysis mode
      None on error
    """
    rc = edgesettings.ShowEdges
    if( mode==1 or mode==2 ): edgesettings.ShowEdges = mode
    if( rc==None ): return scriptcontext.errorhandler()
    return rc


def EnableAutosave( enable=True ):
    """
    Enables or disables Rhino's automatic file saving mechanism
    Parameters:
      enable = the autosave state
    Returns:
      the previous autosave state
    """
    rc = filesettings.AutosaveEnabled
    if (rc != enable): filesettings.AutosaveEnabled = enable
    return rc


def ExeFolder():
    "Returns the full path to Rhino's executable folder."
    return filesettings.ExecutableFolder.FullName


def Exit():
    "Closes the rhino application"
    Rhino.RhinoApp.Exit()


def FindFile(filename):
    """
    Searches for a file using Rhino's search path. Rhino will look for a file
    in the following locations:
      1. The current document's folder.
      2. Folder's specified in Options dialog, File tab.
      3. Rhino's System folders
    Parameters:
      filename = short file name to search for
    Returns:
      full path on success
      None on error
    """
    rc = filesettings.FindFile(filename)
    if( rc==None ): return scriptcontext.errorhandler()
    return rc


def GetPlugInObject( plug_in ):
    """
    Returns a scriptable object from a specified plug-in. Not all plug-ins
    contain scriptable objects. Check with the manufacturer of your plug-in
    to see if they support this capability.
    Parameters:
      plug_in = name or Id of a registered plug-in that supports scripting.
                If the plug-in is registered but not loaded, it will be loaded
    Returns:
      scriptable object if successful
      None on error
    """
    rc = Rhino.RhinoApp.GetPlugInObject(plug_in)
    if( rc==None ): return scriptcontext.errorhandler()
    return rc
  

def InCommand(ignore_runners=True):
    """
    Determines if Rhino is currently running a command. Because Rhino allows
    for transparent commands (commands run from inside of other commands),
    this method returns the total number of active commands.
    Parameters:
      ignore_runners [opt] = If true, script running commands, such as
          LoadScript, RunScript, and ReadCommandFile will not counted.
    Returns:
      the number of active commands
    """
    ids = rhcommand.GetCommandStack()
    return len(ids)


def InstallFolder():
    "The full path to Rhino's installation folder"
    return Rhino.ApplicationSettings.FileSettings.InstallFolder


def IsAlias(alias):
    """
    Verifies that a command alias exists in Rhino
    Parameters:
      the name of an existing command alias
    """
    return aliaslist.IsAlias(alias)


def IsCommand(command_name):
    """
    Verifies that a command exists in Rhino. Useful when scripting commands
    found in 3rd party plug-ins.
    Parameters:
      command_name = the command name to test
    """
    return rhcommand.IsCommand(command_name)


def IsRunningOnWindows():
    "Returns True if this script is being executed on a Windows platform"
    return Rhino.Runtime.HostUtils.RunningOnWindows


def LastCommandName():
    "Returns the name of the last executed command"
    id = rhcommand.LastCommandId
    return rhcommand.LookupCommandName(id, True)


def LastCommandResult():
    """
    Returns the result code for the last executed command
    0 = success (command successfully completed)
    1 = cancel (command was cancelled by the user)
    2 = nothing (command did nothing, but was not cancelled)
    3 = failure (command failed due to bad input, computational problem...)
    4 = unknown command (the command was not found)
    """
    return int(rhcommand.LastCommandResult)


def LocaleID():
    """
    Returns the current language used for the Rhino interface.  The current
    language is returned as a locale ID, or LCID, value.
      1029  Czech
      1031  German-Germany
      1033  English-United States
      1034  Spanish-Spain
      1036  French-France
      1040  Italian-Italy
      1041  Japanese
      1042  Korean
      1045  Polish
    """
    return Rhino.ApplicationSettings.AppearanceSettings.LanguageIdentifier


def Ortho(enable=None):
    """
    Enables or disables Rhino's ortho modeling aid.
    Parameters:
      enable [opt] = the new enabled status (True or False)
    Returns:
      if enable is not specified, then the current ortho status
      if enable is secified, then the previous ortho status
    """
    rc = modelaid.Ortho
    if (enable != None): modelaid.Ortho = enable
    return rc


def Osnap(enable=None):
    """
    Enables or disables Rhino's object snap modeling aid.
    Object snaps are tools for specifying points on existing objects.
    Parameters:
      enable [opt] = the new enabled status (True or False)
    Returns:
      if enable is not specified, then the current osnap status
      if enable is secified, then the previous osnap status
    """
    rc = modelaid.Osnap
    if( enable!=None ): modelaid.Osnap = enable
    return rc


def OsnapDialog(visible=None):
    """
    Shows or hides Rhino's dockable object snap bar
    Parameters:
      visible [opt] = the new visibility state (True or False)
    Returns:
      if visible is not specified, then the current visible state
      if visible is secified, then the previous visible state
    """
    rc = modelaid.UseHorizontalDialog
    if( visible!=None ): modelaid.UseHorizontalDialog = visible
    return rc


def OsnapMode(mode=None):
    """
    Returns or sets the object snap mode. Object snaps are tools for
    specifying points on existing objects
    Parameters:
      mode [opt] = The object snap mode or modes to set. Object snap modes
                   can be added together to set multiple modes
                   0     None
                   1     Near
                   2     Focus
                   4     Center
                   8     Knot
                   16    Quadrant
                   32    Midpoint
                   64    Intersection
                   128   End
                   256   Perpendicular
                   512   Tangent
                   1024  Point
    Returns:
      if mode is not specified, then the current object snap mode(s)
      if mode is specified, then the previous object snap mode(s) 
    """
    rc = modelaid.OSnapModes
    if( mode!=None): modelaid.OSnapModes = mode
    return rc


def Planar(enable=None):
    """
    Enables or disables Rhino's planar modeling aid
    Parameters:
      enable = the new enable status (True or False)
    Returns:
      if enable is not specified, then the current planar status
      if enable is secified, then the previous planar status
    """
    rc = modelaid.Planar
    if( enable!=None ): modelaid.Planar = enable
    return rc


def ProjectOsnaps(enable=None):
    """
    Enables or disables object snap projection
    Parameters:
      enable [opt] = the new enabled status (True or False)
    Returns:
      if enable is not specified, the current object snap projection status
      if enable is specified, the previous object snap projection status
    """
    rc = modelaid.ProjectSnapToCPlane
    if( enable!=None ): modelaid.ProjectSnapToCPlane = enable
    return rc


def Prompt(message=None):
    """
    Change Rhino's command window prompt
    Parameters:
      message [opt] = the new prompt
    """
    if( type!=None and type(message) is not str ):
        strList = [str(item) for item in message]
        message = "".join(strList)
    Rhino.RhinoApp.SetCommandPrompt(message)


def ScreenSize():
    """
    Returns current width and height, of the screen of the primary monitor.
    Returns:
      Tuple containing two numbers identifying the width and height
    """
    sz = System.Windows.Forms.Screen.PrimaryScreen.Bounds
    return sz.Width, sz.Height


def SdkVersion():
    """
    Returns version of the Rhino SDK supported by the executing Rhino.
    Rhino SDK versions are 9 digit numbers in the form of YYYYMMDDn.
    """
    return Rhino.RhinoApp.SdkVersion


def SearchPathCount():
    """
    Returns the number of path items in Rhino's search path list.
    See "Options Files settings" in the Rhino help file for more details.
    """
    return filesettings.SearchPathCount


def SearchPathList():
    """
    Returns all of the path items in Rhino's search path list.
    See "Options Files settings" in the Rhino help file for more details.
    """
    return filesettings.GetSearchPaths()


def SendKeystrokes(keys=None, add_return=True):
    """
    Sends a string of printable characters to Rhino's command line
    Parameters:
      keys [opt] = A string of characters to send to the command line.
      add_returns [opt] = Append a return character to the end of the string.
    """
    Rhino.RhinoApp.SendKeystrokes(keys, add_return)


def Snap(enable=None):
    """
    Enables or disables Rhino's grid snap modeling aid
    Parameters:
      enable [opt] = the new enabled status (True or False)
    Returns:
      if enable is not specified, the current grid snap status
      if enable is specified, the previous grid snap status  
    """
    rc = modelaid.GridSnap
    if( enable!=None ): modelaid.GridSnap = rc
    return rc


def TemplateFile(filename=None):
    """
    Returns or sets Rhino's default template file. This is the template
    file used when Rhino starts.
    Parameters:
      filename[opt] = The name of the new default template file (must exist)
    Returns:
      if filename is not specified, then the current default template file
      if filename is specified, then the previous default template file
    """
    rc = filesettings.TemplateFile
    if filename: filesettings.TemplateFile = filename
    return rc


def TemplateFolder(folder=None):
    """
    Returns or sets the location of Rhino's template folder
    Parameters:
      The location of Rhino's template files. Note, the location must exist
    Returns:
      if folder is not specified, then the current template file folder
      if folder is specified, then the previous template file folder
    """
    rc = filesettings.TemplateFolder
    if folder: filesettings.TemplateFolder = folder
    return rc


def WindowHandle():
    "Returns the windows handle of Rhino's main window"
    return Rhino.RhinoApp.MainWindowHandle()


def WorkingFolder(folder=None):
    """
    Returns or sets Rhino's working directory, or folder.
    The working folder is the default folder for all file operations.
    Parameters:
      folder[opt] = the new working folder
    Returns:
      if folder is not specified, then the current working folder
      if folder is specified, then the previous working folder
    """
    rc = filesettings.WorkingFolder
    if folder: filesettings.WorkingFolder = folder
    return rc