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
        "command": K("escape") + K("colon")
        , "find": K("escape") + K("slash")
        # pages
        , "open": K("escape") + K("t")
        , "open <text>": K("escape") + firefox("tabopen %(text)s", False) + P("20") + K("tab/20,enter")
        , "tropen <text>": K("escape") + firefox("tabopen %(text)s", False) + P("20") + K("tab/20")
        , "tab open": K("escape") + K("o")
        , "tab open <text>": K("escape") + firefox("open %(text)s", False) + P("20") + K("tab/20,enter")
        , "tab tropen <text>": K("escape") + firefox("open %(text)s", False) + P("20") + K("tab/20")
        , "help": K("escape") + firefox("helpall")
        , "reload": K("escape") + K("r")
        , "reload uncached": K("escape") + K("R")
        # tabs
        , "(nexta | righta)": K("escape") + K("g,t")
        , "(preeta | lefta)": K("escape") + K("g,T")
        , "feeta": K("escape") + K("g,0")
        , "latta": K("escape") + K("g,dollar")
        , "clotta": K("escape") + K("d")
        # special pages
        , "home pah": K("escape") + K("g,H")
        , "home page": K("escape") + K("g,h")
        , "page same <website>": K("escape") + K("o") + T("%(website)s") + K("enter")
        , "page <website>": K("escape") + K("t") + T("%(website)s") + K("enter")
        # hint
        , "hint": K("escape") + K("f")
        # bookmarks
        , "book all": K("escape") + T(":bmarks") + K("enter")
        # find
        , "next": K("escape") + K("n")
    }
    defaults = {
                "text":""
    }
    extras = [
        chc_base.text,
        chc_base.website
    ]
