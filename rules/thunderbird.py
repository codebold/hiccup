import choices.base as chc_base

from util import (
    K,
    T,
    P,
    firefox
)

from dragonfly import (
    MappingRule
)

#---------------------------------------------------------------------------
# Core Rule
#---------------------------------------------------------------------------

class CoreRule(MappingRule):
    mapping = {
        "command": K("colon")
        # pages
        , "open": K("t")
        , "open same": K("o")
        , "help": firefox("helpall")
        , "reload": K("r")
        , "reload uncached": K("R")
    }
    defaults = {
        "text":""
    }
    extras = [
        chc_base.text
    ]
