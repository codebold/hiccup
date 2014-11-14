import logging
import time
import traceback

import rules.emacs as emacs
import rules.firefox as firefox
import rules.thunderbird as thunderbird
import rules.shell as shell
import rules.web as web

import loader
import rules.choices.base as chc_base
import rules.choices.web as chc_web

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
    timing_stats("Reload other grammars' rules")

    try:
        reload(chc_base)
        reload(chc_web)
        reload(util)
        reload(emacs)
        reload(web)
        reload(firefox)
        reload(thunderbird)
        reload(shell)

        print '-'*10
        timing_stats("Load other grammars")
        print '-'*10

        grammar = Grammar("Cmd", context=(AppContext(executable="powershell") | AppContext(executable="cmd") | AppContext(executable="sh")))
        grammar.add_rule(shell.ShellCoreRule())
        grammars.append(grammar)

        grammar = Grammar("Putty", context=AppContext(executable="putty"))
        grammar.add_rule(emacs.EmacsBaseRule())
        grammar.add_rule(emacs.EmacsCoreRule())
        grammar.add_rule(emacs.EshellRule())
        grammar.add_rule(emacs.DiredRule())
        grammar.add_rule(shell.ShellCoreRule())
        grammar.add_rule(shell.GitRule())
        grammars.append(grammar)
    
        grammar = Grammar("Firefox", context=AppContext(executable="firefox"))
        grammar.add_rule(firefox.CoreRule())
        grammars.append(grammar)

        grammar = Grammar("Thunderbird", context=AppContext(executable="thunderbird"))
        grammar.add_rule(thunderbird.CoreRule())
        grammars.append(grammar)

        grammar = Grammar("Emacs", context=AppContext(executable="emacs"))
        grammar.add_rule(emacs.EmacsCoreRule())
        grammar.add_rule(emacs.EmacsBaseRule())
        grammar.add_rule(emacs.EshellRule(context=AppContext(title="- EShell -")))
        grammar.add_rule(emacs.DiredRule())
        grammar.add_rule(shell.ShellCoreRule(context=AppContext(title="- EShell -")))
        grammar.add_rule(shell.GitRule(context=AppContext(title="- EShell -")))
        grammar.add_rule(web.HtmlCoreRule(context=AppContext(title="- Web -")))
        grammar.add_rule(web.HtmlTemplateRule(context=AppContext(title="- Web -")))
        grammar.add_rule(emacs.HtmlRule(context=AppContext(title="- Web -")))
        grammar.add_rule(web.CssCoreRule(context=AppContext(title="- CSS -")))
        grammars.append(grammar)

        grammarLoader = loader.GrammarLoader(grammars)
        grammarLoader.load()
    except:
        print '-'*10
        traceback.print_exc()
        return

    print '-'*10
    timing_stats("Time to setup other grammars")

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
