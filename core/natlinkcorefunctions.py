#
# Python Macro Language for Dragon NaturallySpeaking
#   (c) Copyright 1999 by Joel Gould
#   Portions (c) Copyright 1999 by Dragon Systems, Inc.
#
"""natlinkcorefunctions.py

 Quintijn Hoogenboom, January 2008:

These functions are used by natlinkstatus.py,
and can also used by all the modules,
as the core folder will be in the python path
when natlink is running.

The first function is also, hopefully identical, in
natlinkconfigfunctions, in the configurenatlinkvocolaunimacro folder

getBaseFolder: returns the folder from the calling module
getCoreDir: returns the core folder of natlink, relative to the configure directory
fatalError: raises error again, if new_raise is set, otherwise continues executing
getExtendedEnv(env): gets from os.environ, or from window system calls (CSIDL_...) the
                     environment. Take PERSONAL for HOME and ~
getAllFolderEnvironmentVariables: get a dict of all possible HOME and CSIDL variables,
           that result in a valid folder path
substituteEnvVariableAtStart: substitute back into a file/folder path an environment variable



""" 
import os, sys, re, copy
from win32com.shell import shell, shellcon
import win32api
# for extended environment variables:
reEnv = re.compile('(%[A-Z_]+%)', re.I)

def getBaseFolder(globalsDict=None):
    """get the folder of the calling module.

    either sys.argv[0] (when run direct) or
    __file__, which can be empty. In that case take the working directory
    """
    globalsDictHere = globalsDict or globals()
    baseFolder = ""
    if globalsDictHere['__name__']  == "__main__":
        baseFolder = os.path.split(sys.argv[0])[0]
##        print 'baseFolder from argv: %s'% baseFolder
    elif globalsDictHere['__file__']:
        baseFolder = os.path.split(globalsDictHere['__file__'])[0]
##        print 'baseFolder from __file__: %s'% baseFolder
    if not baseFolder:
        baseFolder = os.getcwd()
##        print 'baseFolder was empty, take wd: %s'% baseFolder
    return baseFolder

# report function:
def fatal_error(message, new_raise=None):
    """prints a fatal error when running this module"""
    print 'natlinkconfigfunctions fails because of fatal error:'
    print
    print message
    print
    print 'Exit Dragon and run the configurenatlink program (via start_configurenatlink.py)'
    print 
    if new_raise:
        raise new_raise
    else:
        raise

# keep track of found env variables, fill, if you wish, with
# getAllFolderEnvironmentVariables.
# substitute back with substituteEnvVariableAtStart.
# and substite forward with expandEnvVariableAtStart
# in all cases a private envDict can be user, or the global dict recentEnv
#
# to collect all env variables, call getAllFolderEnvironmentVariables, see below
recentEnv = {}

def getExtendedEnv(var, envDict=None, displayMessage=1):
    """get from environ or windows CSLID

    HOME is environ['HOME'] or CSLID_PERSONAL
    ~ is HOME

    As envDict for recent results either a private (passed in) dict is taken, or
    the global recentEnv.

    This is merely for "caching results"

    """
    if envDict == None:
        myEnvDict = recentEnv
    else:
        myEnvDict = envDict
##    var = var.strip()
    var = var.strip("% ")
    var = var.upper()
    
    if var == "~":
        var = 'HOME'

    if var in myEnvDict:
        return myEnvDict[var]

    if var in os.environ:
        myEnvDict[var] = os.environ[var]
        return myEnvDict[var]

    # try to get from CSIDL system call:
    if var == 'HOME':
        var2 = 'PERSONAL'
    else:
        var2 = var
        
    try:
        CSIDL_variable =  'CSIDL_%s'% var2
        shellnumber = getattr(shellcon,CSIDL_variable, -1)
    except:
        print 'getExtendedEnv, cannot find in environ or CSIDL: "%s"'% var2
        return ''
    if shellnumber < 0:
        # on some systems have SYSTEMROOT instead of SYSTEM:
        if var == 'SYSTEM':
            return getExtendedEnv('SYSTEMROOT', envDict=envDict)
        raise ValueError('getExtendedEnv, cannot find in environ or CSIDL: "%s"'% var2)
    try:
        result = shell.SHGetFolderPath (0, shellnumber, 0, 0)
    except:
        if displayMessage:
            print 'getExtendedEnv, cannot find in environ or CSIDL: "%s"'% var2
        return ''

    
    result = str(result)
    result = os.path.normpath(result)
    myEnvDict[var] = result
    # on some systems apparently:
    if var == 'SYSTEMROOT':
        myEnvDict['SYSTEM'] = result
    return result

def clearRecentEnv():
    """for testing, clears above global dictionary
    """
    recentEnv.clear()

def getAllFolderEnvironmentVariables(fillRecentEnv=None):
    """return, as a dict, all the environ AND all CSLID variables that result into a folder
    
    TODO:  Also include NATLINK, UNIMACRO, VOICECODE, DRAGONFLY, VOCOLAUSERDIR, UNIMACROUSERDIR

    Optionally put them in recentEnv, if you specify fillRecentEnv to 1 (True)

    """
    global recentEnv
    D = {}

    for k in dir(shellcon):
        if k.startswith("CSIDL_"):
            kStripped = k[6:]
            try:
                v = getExtendedEnv(kStripped, displayMessage=None)
            except ValueError:
                continue
            if len(v) > 2 and os.path.isdir(v):
                D[kStripped] = v
            elif v == '.':
                D[kStripped] = os.getcwd()
    # os.environ overrules CSIDL:
    for k in os.environ:
        v = os.environ[k]
        if os.path.isdir(v):
            v = os.path.normpath(v)
            if k in D and D[k] != v:
                print 'warning, CSIDL also exists for key: %s, take os.environ value: %s'% (k, v)
            D[k] = v
            
    if fillRecentEnv:
        recentEnv = copy.copy(D)
    return D

#def setInRecentEnv(key, value):
#    if key in recentEnv:
#        if recentEnv[key] == value:
#            print 'already set (the same): %s, %s'% (key, value)
#        else:
#            print 'already set (but different): %s, %s'% (key, value)
#        return
#    print 'setting in recentEnv: %s to %s'% (key, value)
#    recentEnv[key] = value
            

def substituteEnvVariableAtStart(filepath, envDict=None): 
    """try to substitute back one of the (preused) environment variables back

    into the start of a filename

    if ~ (HOME) is D:\My documents,
    the path "D:\My documents\folder\file.txt" should return "~\folder\file.txt"

    pass in a dict of possible environment variables, which can be taken from recent calls, or
    from  envDict = getAllFolderEnvironmentVariables().

    Alternatively you can call getAllFolderEnvironmentVariables once, and use the recentEnv
    of this module! getAllFolderEnvironmentVariables(fillRecentEnv)

    If you do not pass such a dict, recentEnv is taken, but this recentEnv holds only what has been
    asked for in the session, so no complete list!

    """
    if envDict == None:
        envDict = recentEnv
    Keys = envDict.keys()
    # sort, longest result first, shortest keyname second:
    decorated = [(-len(envDict[k]), len(k), k) for k in Keys]
    decorated.sort()
    Keys = [k for (dummy1,dummy2, k) in decorated]
    for k in Keys:
        val = envDict[k]
        if filepath.lower().startswith(val.lower()):
            if k in ("HOME", "PERSONAL"):
                k = "~"
            else:
                k = "%" + k + "%"
            filepart = filepath[len(val):]
            filepart = filepart.strip('/\\ ')
            return os.path.join(k, filepart)
    # no hit, return original:
    return filepath
       
def expandEnvVariableAtStart(filepath, envDict=None): 
    """try to substitute environment variable into a path name

    """
    filepath = filepath.strip()

    if filepath.startswith('~'):
        folderpart = getExtendedEnv('~', envDict)
        filepart = filepath[1:]
        filepart = filepart.strip('/\\ ')
        return os.path.normpath(os.path.join(folderpart, filepart))
    elif reEnv.match(filepath):
        envVar = reEnv.match(filepath).group(1)
        # get the envVar...
        try:
            folderpart = getExtendedEnv(envVar, envDict)
        except ValueError:
            print 'invalid (extended) environment variable: %s'% envVar
        else:
            # OK, found:
            filepart = filepath[len(envVar)+1:]
            filepart = filepart.strip('/\\ ')
            return os.path.normpath(os.path.join(folderpart, filepart))
    # no match
    return filepath
    
def expandEnvVariables(filepath, envDict=None): 
    """try to substitute environment variable into a path name,

    ~ only at the start,

    %XXX% can be anywhere in the string.

    """
    filepath = filepath.strip()
    
    if filepath.startswith('~'):
        folderpart = getExtendedEnv('~', envDict)
        filepart = filepath[1:]
        filepart = filepart.strip('/\\ ')
        filepath = os.path.normpath(os.path.join(folderpart, filepart))
    
    if reEnv.search(filepath):
        List = reEnv.split(filepath)
        #print 'parts: %s'% List
        List2 = []
        for part in List:
            try:
                folderpart = getExtendedEnv(part, envDict)
            except ValueError:
                folderpart = part
            List2.append(folderpart)
        filepath = ''.join(List2)
        return os.path.normpath(filepath)
    # no match
    return filepath

class InifileSection(object):
    """simulate a part of the registry through inifiles
    
        basic file is natlinkstatus.ini
        basic section is usersettings
        
        So one instance operates only on one section of one ini file!
        
        other instances can be opened by giving the filename
        and/or the section
        
        methods:
        set(key, value): set a key=value entry in the section
        get(key, defaultValue=None): get the associated value with
                 key in the current section.
                 if empty or not there, the defaultValue is returned
                 if value = "0" or "1" the integer value 0 or 1 is returned
        delete(key): deletes from section
        keys(): return a list of keys in the section
        
        
    """
    def __init__(self, section, filename):
        """open a section in a inifile
        
        """
        dirName, filePart = os.path.split(filename)
        if not os.path.isdir(dirName):
            raise ValueError("InifileSection, filename should be in a valid directory, not: %s"% dirName)
        self.filename = filename
        self.firstUse = (not os.path.isfile(self.filename))
        self.section =  section
            
    def get(self, key, defaultValue=None):
        """get an item from a key
        
        """
        if defaultValue is None:
            defaultValue = ''
        else:
            defaultValue = str(defaultValue)
        value = win32api.GetProfileVal(self.section, key, defaultValue, self.filename)
##        if value:
##            print 'get: %s, %s: %s'% (self.section, key, value)
        if value in ("0", "1"):
            return int(value)
        return value

    def set(self, key, value):
        """set an item for akey
        
        """
##        print 'set: %s, %s: %s'% (self.section, key, value)
        win32api.WriteProfileVal( self.section, key, value, self.filename)
        checkValue = win32api.GetProfileVal(self.section, key, 'nonsens', self.filename)
        if not (checkValue == value or \
                          value in [0, 1] and checkValue == str(value)):
            print 'set failed:  %s, %s: %s, got %s instead'% (self.section, key, value, checkValue)

    def delete(self, key):
        """delete an item for a key (really set to "")
        
        """
        print 'delete: %s, %s'% (self.section, key)
        value = win32api.WriteProfileVal( self.section, key, None,
                                       self.filename)
        checkValue = win32api.GetProfileVal(self.section, key, 'nonsens', self.filename)
        if checkValue != 'nonsens':
            print 'delete failed:  %s, %s: got %s instead'% (self.section, key, checkValue)

    def keys(self):
        Keys =  win32api.GetProfileSection( self.section, self.filename)
        Keys = [k.split('=')[0].strip() for k in Keys]
        #print 'return Keys: %s'% Keys
        return Keys

defaultFilename = "natlinkstatus.ini"
defaultSection = 'usersettings'
class NatlinkstatusInifileSection(InifileSection):
    """subclass with fixed filename and section"""
    
    def __init__(self):
        """get the default inifile:
        In baseDirectory (this directory) the ini file natlinkstatus.ini
        with section defaultSection
        """        
        dirName = getBaseFolder()
        if not os.path.isdir(dirName):
            raise ValueError("starting inifilesection, invalid directory: %s"%
                            dirName)
        filename = os.path.join(dirName, defaultFilename)
        InifileSection.__init__(self, section=defaultSection, filename=filename)


if __name__ == "__main__":
    print 'this module is in folder: %s'% getBaseFolder(globals())
    vars = getAllFolderEnvironmentVariables()
    print 'allfolderenvironmentvariables:  %s'% vars.keys()
    for k,v in vars.items():
        print '%s: %s'% (k, v)

    print 'testing       expandEnvVariableAtStart'  
    for p in ("D:\\natlink\\unimacro", "~/unimacroqh",
              "%HOME%/personal",
              "%WINDOWS%\\folder\\strange testfolder"):
        expanded = expandEnvVariableAtStart(p)
        print 'expandEnvVariablesAtStart: %s: %s'% (p, expanded)
    print 'testing       expandEnvVariables'  
    for p in ("D:\\%username%", "D:\\natlink\\unimacro", "~/unimacroqh",
              "%HOME%/personal",
              "%WINDOWS%\\folder\\strange testfolder"):
        expanded = expandEnvVariables(p)
        print 'expandEnvVariables: %s: %s'% (p, expanded)

