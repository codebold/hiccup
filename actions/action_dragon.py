import os
import time

from subprocess import call

from natlink import (
    setMicState
)

from dragonfly import (
    ActionBase,
    Pause,
    FocusWindow,
    Window
)

GRAMMAR_DIRECTORY = "c:\Python\NatLink\NatLink\MacroSystem"
TOUCH_BIN = "c:/Program Files (x86)/Git/bin/touch.exe"

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


#---------------------------------------------------------------------------
# NatLink
#---------------------------------------------------------------------------

# Those function will only work on a 32bit machine...
def blitz_natlink_status():
    win = Window.get_foreground()
    FocusWindow(executable="natspeak", title="Messages from NatLink").execute()
    Pause("100").execute()
    win.set_foreground()

def show_natlink_status():
    FocusWindow(executable="natspeak", title="Messages from NatLink").execute()
