import logging 
import time
import traceback

import builder
import loader

import rules.base as base
import rules.firefox as firefox
import rules.choices.base as chc_base

from dragonfly import (
    AppContext
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
    reload(firefox)

    timing_stats("Load base grammar")

    grammars.append(
        builder.GrammarBuilder("Base", context=AppContext())
        .add_rule(base.CharacterRule())
        .add_rule(base.LiteralRule())
        .add_rule(base.StandardKeysRule())
        .add_rule(base.NavigatingKeysRule())
        .add_rule(base.MetaKeysRule())
        .add_competitive_mapping_rule(base.ShortcutRule(), [firefox.ShortcutRule(context=AppContext(executable="firefox"))])
        # .add_competitive_repeat_rule(builder.RepeatRuleComponents(None, [base.CharacterRule(), base.LiteralRule(), base.StandardKeysRule(), base.NavigatingKeysRule(), base.MetaKeysRule(), base.ShortcutRule()]), [builder.RepeatRuleComponents(AppContext(executable="firefox"), [None, None, None, None, None, firefox.KeyboardRule()])])
        .add_rule(base.DictationRule())
        .add_rule(base.FormattedDictationRule())
        .add_rule(base.PhraseRule())
        .add_rule(base.WindowsRule())
        .add_rule(base.DragonRule())
        .build()
    )
        
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
