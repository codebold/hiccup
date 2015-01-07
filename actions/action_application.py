from dragonfly import ActionBase

from action_shortcut import (
    T,
    K,
    P
)

from action_base import (
    ActionSeries,
    ExtensibleRepeatedText
)

class ApplicationActionBase(ExtensibleRepeatedText):

    _submit = True
    _invoke_action = None
    _submit_action = K("enter")

    def __init__(self, spec=None, submit=True, static=False):
        super(ApplicationActionBase, self).__init__(spec, static, pause=None, autofmt=False)
        _submit = submit

    def _execute_before_keyboard_events(self):
        if isinstance(self._invoke_action, ActionBase):
            self._invoke_action.execute()

    def _execute_after_keyboard_events(self):
        if self._submit:
            self._submit_action.execute()

#---------------------------------------------------------------------------
# Windows CMD
#---------------------------------------------------------------------------

class WinCmd(ApplicationActionBase):

    _invoke_action = ActionSeries(K("w-r"), P("20"))

#---------------------------------------------------------------------------
# Emacs Command
#---------------------------------------------------------------------------

class Emacs(ApplicationActionBase):
    
    _invoke_action = K("a-u")

#---------------------------------------------------------------------------
# Firefox
#---------------------------------------------------------------------------

class Firefox(ApplicationActionBase):
    
    _invoke_action = K("colon")
