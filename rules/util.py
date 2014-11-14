import os
import string
import time
import collections
import types

from subprocess import (
    call
)

from dragonfly import (
    ActionBase,
    Text,
    Key,
    Pause,
    Mouse,
    FocusWindow,
    Window
)

from natlink import (
    setMicState
)

GRAMMAR_DIRECTORY = "c:\Python\NatLink\NatLink\MacroSystem"
TOUCH_BIN = "c:/Program Files (x86)/Git/bin/touch.exe"

#---------------------------------------------------------------------------
# Shortcuts
#---------------------------------------------------------------------------

def T(s, pause=0.00001, **kws):
    return Text(s, pause=pause, **kws)

def K(*args, **kws):
    return Key(*args, **kws)

def P(*args, **kws):
    return Pause(*args, **kws)

def M(*args, **kws):
    return Mouse(*args, **kws)



#---------------------------------------------------------------------------
# Grammar update
#---------------------------------------------------------------------------

# Those function will only work on a 32bit machine...
def blitz_natlink_status():
    win = Window.get_foreground()
    FocusWindow(executable="natspeak", title="Messages from NatLink").execute()
    Pause("100").execute()
    win.set_foreground()

def show_natlink_status():
    FocusWindow(executable="natspeak", title="Messages from NatLink").execute()
    
#---------------------------------------------------------------------------
# Windows Command Runners
#---------------------------------------------------------------------------

class WindowsCommand(ActionBase):
    _Command = None

    def __init__(self, command):
        super(ActionBase, self).__init__()
        self._command = command

    def _execute(self, data):
        print "hello"
    

def windows(command, shell=True):
    print command
    return call(command, shell)

#---------------------------------------------------------------------------
# Emacs Command Runners
#---------------------------------------------------------------------------

class EmacsCommand(ActionBase):
    _command = None
    _narg = None

    def __init__(self, command, narg=None):
        super(ActionBase, self).__init__()
        self._command = command
        self._narg = narg
        self._str = command

    def _execute(self, data):
        reps = data.get(self._narg, 1)
        for _i in xrange(reps):
            K("a-u").execute() 
            #   Key("a-x")  is smex
            T("%s\n"%self._command, pause=0.00001).execute()

def emacs(command, narg=None):
    if not narg:
        if command.startswith("("):
            return (K("a-u") #   Key("a-x")  is smex
                    + T("eval-expression\n%s\n"%command, pause=0.00001))
        else:
            return (K("a-u") + Text("%s\n"%command, pause=0.00001))
    else:
        return EmacsCommand(command=command, narg=narg)

#---------------------------------------------------------------------------
# Firefox Command
#---------------------------------------------------------------------------

class FirefoxCommand(ActionBase):
    _command = None
    _submit = False

    def __init__(self, command, submit):
        super(ActionBase, self).__init__()
        self._command = command
        self._submit = submit
        self._str = command

    def _execute(self, data):
        command = self._command % data
        K("colon").execute()
        T(command).execute()
        if self._submit:
            K("enter").execute()

def firefox(command, submit=True):
    return FirefoxCommand(command, submit)

#---------------------------------------------------------------------------
# Grammar update
#---------------------------------------------------------------------------

class GrammarUpdate(ActionBase):

    _touch_bin = TOUCH_BIN
    _grammar_directory = GRAMMAR_DIRECTORY
    
    def __init__(self):
        super(ActionBase, self).__init__()
        self._str = "update grammar"

    def _execute(self, data):
        grammar = "%(grammar)s" % data

        if not grammar.endswith(".py"):
            grammar += ".py"
            
        touch("{0}/{1}".format(self._grammar_directory, grammar), self._touch_bin)
        setMicState("sleeping")
        time.sleep(0.2)
        setMicState("on")

def updateGrammar(narg=None):
    return GrammarUpdate()


def updateAllGrammars(grammar_directory=GRAMMAR_DIRECTORY, touch_bin=TOUCH_BIN):
    for file in os.listdir(grammar_directory):
        if file.endswith(".py"):
            touch("{0}/{1}".format(grammar_directory, file), touch_bin)
    setMicState("sleeping")
    time.sleep(0.2)
    setMicState("on")
            
                        

def touch(file_path, touch_bin=TOUCH_BIN):
    return call('"{0}" "{1}"'.format(touch_bin, file_path), shell=True)
