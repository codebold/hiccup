import logging
import time
import traceback

from dragonfly import AppContext

import grammar.builder as builder
import grammar.loader as loader

import rules.emacs as emacs
import rules.firefox as firefox
import rules.thunderbird as thunderbird
import rules.shell as shell
import rules.vim as vim
import rules.web as web
import rules.choices.base as chc_base
import rules.choices.web as chc_web

#---------------------------------------------------------------------------
# Setup
#---------------------------------------------------------------------------

logging.basicConfig() 

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

    reload(chc_base)
    reload(chc_web)
    reload(emacs)
    reload(web)
    reload(firefox)
    reload(thunderbird)
    reload(shell)

    timing_stats("Load other grammars")

    grammars.append(
        builder.GrammarBuilder("Cmd", context=(AppContext(executable="powershell")
                                               | AppContext(executable="cmd")
                                               | AppContext(executable="sh")))
        .add_rule(shell.ShellCoreRule())
        .add_rule(shell.GitRule())        
        .build()
    )

    grammars.append(
        builder.GrammarBuilder("Putty", context=AppContext(executable="putty"))
        .add_rule(emacs.EmacsCoreRule(context=AppContext(title="emacs")))
        .add_rule(emacs.EshellRule(context=AppContext(title="emacs")))
        .add_rule(emacs.DiredRule(context=AppContext(title="emacs")))
        .add_rule(vim.VimCoreRule(context=AppContext(title="vi")))
        .add_rule(shell.ShellCoreRule())
        .add_rule(shell.GitRule())
        .build()
    )
            
    grammars.append(
        builder.GrammarBuilder("Firefox", context=AppContext(executable="firefox"))
        .add_rule(firefox.FirefoxCoreRule())
        .build()
    )

    grammars.append(
        builder.GrammarBuilder("Thunderbird", context=AppContext(executable="thunderbird"))
        .add_rule(thunderbird.ThunderbirdCoreRule())
        .build()
    )

    grammars.append(
        builder.GrammarBuilder("Emacs", context=AppContext(executable="emacs"))
        .add_rule(emacs.EmacsCoreRule())
        .add_rule(emacs.DiredRule())
        .add_rule(emacs.ErcRule())
        .add_rule(emacs.EshellRule(context=AppContext(title="- EShell -")))
        .add_rule(shell.ShellCoreRule(context=AppContext(title="- EShell -")))
        .add_rule(shell.GitRule(context=AppContext(title="- EShell -")))
        .add_rule(web.HtmlCoreRule(context=AppContext(title="- Web -")))
        .add_rule(web.HtmlTemplateRule(context=AppContext(title="- Web -")))
        .add_rule(emacs.EmacsHtmlRule(context=AppContext(title="- Web -")))
        .add_rule(web.CssCoreRule(context=AppContext(title="- CSS -")))
        .add_rule(shell.IrcRule(context=AppContext(title="- ERC -")))
        .build()
    )

    grammarLoader = loader.GrammarLoader(grammars)
    grammarLoader.load()

    print '-'*10
    timing_stats("Time to setup other grammars")

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
