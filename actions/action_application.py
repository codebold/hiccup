from subprocess import call

from dragonfly import ActionBase

from action_shortcut import (
    T,
    K
)

#---------------------------------------------------------------------------
# Windows Command
#---------------------------------------------------------------------------

class WindowsCommand(ActionBase):

    def __init__(self, command, shell=True, narg=None):
        super(ActionBase, self).__init__()
        self._command = command
        self._shell = shell
        self._narg = narg
        self._str = command

    def _execute(self, data):
        reps = data.get(self._narg, 1)
        for i in xrange(reps):
            call(self._command, self._shell)
            

def windows(command, shell=True, narg=None):
    return WindowsCommand(command, shell, narg)

#---------------------------------------------------------------------------
# Emacs Command
#---------------------------------------------------------------------------

class EmacsCommand(ActionBase):

    def __init__(self, command, narg=None):
        super(ActionBase, self).__init__()
        self._command = command
        self._narg = narg
        self._str = command

    def _execute(self, data):
        reps = data.get(self._narg, 1)
        for i in xrange(reps):
            K("a-u").execute() 
            #   Key("a-x")  is smex
            T("%s\n"%self._command, pause=0.00001).execute()

def emacs(command, narg=None):
    if not narg:
        if command.startswith("("):
            return (K("a-u") #   Key("a-x")  is smex
                    + T("eval-expression\n%s\n"%command, pause=0.00001))
        else:
            return (K("a-u") + T("%s\n"%command, pause=0.00001))
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
