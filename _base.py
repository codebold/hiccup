import logging 
import time
import traceback

from dragonfly import AppContext

import grammar.builder as builder
import grammar.loader as loader

import rules.base as base
import rules.emacs as emacs
import rules.firefox as firefox
import rules.vim as vim
import rules.choices.base as chc_base

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
    reload(base)
    reload(firefox)
    reload(emacs)

    timing_stats("Load base grammar")

    grammars.append(
        builder.GrammarBuilder("Base", context=AppContext())
        .add_competitive_repeat_rule(
            builder.RepeatRuleComponents(
                "Base",
                None,
                [
                    base.CharacterRule(),
                    base.LiteralRule(),
                    base.StandardKeysRule(),
                    base.NavigatingKeysRule(),
                    base.MetaKeysRule(),
                    base.ShortcutRule()
                ]
            ),
            [
                builder.RepeatRuleComponents(
                    "Base (Firefox)",
                    AppContext(executable="firefox"),
                    [
                        None,
                        None,
                        None,
                        None,
                        None,
                        firefox.FirefoxShortcutRule()
                    ]
                ),
                # Combining the contexts of "Base (Emacs) and Base (Emacs via Putty)" with a logical or operator crashes natspeak.exe
                # TODO: Check why this happens...
                builder.RepeatRuleComponents(
                    "Base (Emacs)",
                    AppContext(executable="emacs"),
                    [
                        None,
                        None,
                        None,
                        emacs.EmacsNavigatingKeysRule(),
                        None,
                        emacs.EmacsShortcutRule()
                    ]
                ),
                builder.RepeatRuleComponents(
                    "Base (Emacs via Putty)",
                    AppContext(executable="putty", title="emacs"),
                    [
                        None,
                        None,
                        None,
                        emacs.EmacsNavigatingKeysRule(),
                        None,
                        emacs.EmacsShortcutRule()
                    ]
                ),
                builder.RepeatRuleComponents(
                    "Base (Vim via Putty)",
                    AppContext(executable="putty", title="vi"),
                    [
                        None,
                        None,
                        None,
                        vim.VimNavigatingKeysRule(),
                        None,
                        vim.VimShortcutRule()
                    ]
                )
            ]
        )
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
    print '-'*10
    traceback.print_exc()
    
    try:
        unload()
    except:
        # sometimes during a module reload unload becomes None
        pass
    raise
