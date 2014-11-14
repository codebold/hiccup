import logging 
import time
import traceback

import rules.base as base

import loader
import rules.choices.base as chc_base

from dragonfly import (
    AppContext,
    Grammar
)

import rules.util as util

#---------------------------------------------------------------------------
# Setup
#---------------------------------------------------------------------------
logging.basicConfig() 
#logging.basicConfig(level=10)
grammarLoader = None
init_time = time.time()

def timing_stats(msg):
    print '%s:'%msg, (time.time() - init_time)

#---------------------------------------------------------------------------
# Loading
#---------------------------------------------------------------------------

# Unload function which will be called by natlink at unload time.
def unload():
    if grammarLoader:
        try:
            grammarLoader.unload()
        except:
            traceback.print_exc()

# Create this module's grammars.
def load():
    grammars = []

    print '-'*10
    timing_stats("Reload base grammar's rules")
    
    reload(chc_base)
    reload(util)
    reload(base)

    timing_stats("Load base grammar")
    
    grammar = Grammar("Base", context=AppContext())
    grammar.add_rule(base.RepeatRule())
    grammar.add_rule(base.FormattedDictationRule())
    grammar.add_rule(base.CharacterDictationRule())
    grammar.add_rule(base.WindowsRule())
    grammar.add_rule(base.DragoflyRule())
    grammars.append(grammar)
    
    grammarLoader = loader.GrammarLoader(grammars)
    grammarLoader.load()

    timing_stats("Time to setup base grammar")
    print '-'*10
    
#---------------------------------------------------------------------------
# Main
#---------------------------------------------------------------------------
try:
    load()
except:
    try:
        unload()
    except:
        # sometimes during a module reload unload becomes None
        pass
    raise
