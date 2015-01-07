from dragonfly import MappingRule

from actions.action_application import Firefox
from actions.action_shortcut import (
    K,
    T,
    P
)

import choices.base as chc_base

#---------------------------------------------------------------------------
# Core Rule
#---------------------------------------------------------------------------

class ThunderbirdCoreRule(MappingRule):
    mapping = {
        "command": K("colon")
        # pages
        , "open": K("t")
        , "open same": K("o")
        , "help": Firefox("helpall")
        , "reload": K("r")
        , "reload uncached": K("R")
    }
    defaults = {
        "text":""
    }
    extras = [
        chc_base.text
    ]
