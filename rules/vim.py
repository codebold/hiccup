from dragonfly import MappingRule

from actions.action_application import Vim
from actions.action_shortcut import (
    K,
    T,
    P
)

import choices.base as chc_base

#---------------------------------------------------------------------------
# Keyboard
#---------------------------------------------------------------------------

class VimNavigatingKeysRule(MappingRule):
    mapping = {
        # Words
        "foo [<1to100>]": K("w:%(1to100)d")
        , "sell foo [<1to100>]": K("v, w:%(1to100)d")
        , "dee foo [<1to100>]": K("v, w:%(1to100)d, d")
        , "bar [<1to100>]": K("b:%(1to100)d")
        , "sell bar [<1to100>]": K("v, b:%(1to100)d")
        , "dee bar [<1to100>]": K("v, b:%(1to100)d, d")
        , "sellword [<1to100>]": K("v") + K("sc-right:%(1to100)d")
        # Lines
        , "sellome": K("v, home")
        , "deelome": K("v, home, d")
        , "sellend": K("v, end")
        , "deelend": K("v, end, d")
        , "cleeline": K("escape")
        , "selline [<0to100>]": K("home, v,down:%(0to100)d, end")
        , "deeline [<0to100>]": K("home, v,down:%(0to100)d, end, d")
        , "coline [<0to100>]": K("home, v,down:%(0to100)d, end, y")
        , "dupline  [<0to100>] [<1to10>]": K("home, v,down:%(0to100)d, end, y") + P("20") + K("enter, p:%(1to10)d")
        # Pages
        , "go to home": K("g:2")
        , "go to end": K("G")
        , "sell-all": K("g:2,V,G")
    }
    defaults = {
        "0to100":0,
        "1to10":1,
        "1to100":1
    }
    extras = [
        chc_base._0to100,
        chc_base._1to10,
        chc_base._1to100
    ]

class VimShortcutRule(MappingRule):
    mapping = {
        # general
        "quit [<1to100>]": K("escape:%(1to100)d")
        , "(cop | copy) [<1to100>]": K("y:%(1to100)d")
        , "cut [<1to100>]": K("d:%(1to100)d")
        , "paste [<1to100>]": K("p:%(1to100)d")
        , "(undo | scratch) [<1to100>]": K("escape, u:%(1to100)d")
        , "redo [<1to100>]": K("escape, c-r:%(1to100)d")
        , "find [<1to100>]": K("slash:%(1to100)d")
        , "find now <text>": K("slash") + T('%(text)s')
        , "close": K("escape, colon, q, enter")
        # files
        , "(nuphyle | new file)": Vim("n")
        , "(ophyle |  open file)": Vim("e")
        , "(saphyle | save file)": Vim("w")
        , "(saphylas | save file as)": Vim("saveas")
    }
    defaults = {
        "text":"",
        "1to100":1
    }
    extras = [
        chc_base.text,
        chc_base._1to100
    ]

#---------------------------------------------------------------------------
# Core Rule
#---------------------------------------------------------------------------

class VimCoreRule(MappingRule):
    mapping = {
        "command": K("escape,colon")
        , "closave": K("escape, colon, w, q, enter")
        , "closover": K("escape, colon, w, exclamation, q, enter")
        , "closard": K("escape, colon, q, exclamation, enter")
        }
    defaults = {
        "text":""
    }
    extras = [
        chc_base.text
    ]
