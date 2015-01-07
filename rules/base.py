import natlink

from dragonfly import (
    MappingRule,
    CompoundRule,
    RuleRef,
    IntegerRef,
    Alternative,
    Repetition,
    Function,
    StartApp,
    BringApp
)

from actions.action_application import WinCmd
from actions.action_dragon import (
    updateGrammar,
    updateAllGrammars,
    GrammarUpdate,
    blitz_natlink_status,
    show_natlink_status
)
from actions.action_dynstartapp import DynStartApp
from actions.action_shortcut import (
    K,
    T,
    P
)

import choices.base as chc_base

#---------------------------------------------------------------------------
# Characters
#---------------------------------------------------------------------------
class CharacterRule(MappingRule):
    mapping = {}
    for word in chc_base.alpha_words:
        letter = word[0].lower()
        mapping[word] = K(letter)
        mapping['cap ' +word] = K(letter.upper())
        mapping['insert ' +word] = T(word.lower())

# NatSpeak's spell command already does this job.       
class SpellingRule(CompoundRule):
    spec = "(letters|spell) <letter_sequence>"
    extras = [Repetition(chc_base.letter,
                         min=1, max=26,
                         name="letter_sequence")]

    def _process_recognition(self, node, extras):
        for letter in extras["letter_sequence"]:
            T(letter).execute()

class LiteralRule(MappingRule):
    mapping = {
        "(num | N.) <0to10000>":T("%(0to10000)s")
        , "<0to10000> dot <0to100>":T("%(0to10000)s.%(0to100)s")
        , "<operator> <0to10000>":T("%(operator)s%(0to10000)s")
        , "AM":T("am")
        , "PM":T("pm")
        , "[time] <0to12> [<0to60>] <time_period>":T("%(0to12)d:%(0to60)02d%(time_periods")
    }
    defaults = {
        "0to60":0
        , "time_period":"am"
    }
    extras = [
        chc_base._0to60
        , chc_base._0to12
        , chc_base._0to100
        , chc_base._0to10000
        , chc_base.time_period
        , chc_base.operator
    ]

#---------------------------------------------------------------------------
# Keyboard
#---------------------------------------------------------------------------

class StandardKeysRule(MappingRule):
    mapping = {
        "(space | ace ) [<1to100>]": K("space")
        , "slap [<1to100>]": K("enter:%(1to100)d")        
        , "(tap | tab) [<1to100>]": K("tab:%(1to100)d")
        , "escape [<1to100>]": K("escape:%(1to100)d")
        , "backspace [<1to100>]": K("backspace:%(1to100)d")
        , "delete [<1to100>]": K("delete:%(1to100)d")
        # punctuation
        , "(dot | period) [<1to100>]": K("dot:%(1to100)d")
        , "(comma | cam)": K("comma")
        , "(colon|coal) [<1to100>]": K("colon:%(1to100)d")
        , "(semi colon|sem-col|sem-coal)": T(";")
        , "(exclaim|clam)": K("exclamation")
        , "(question-mark|quest)": K("question")
        , "slash": K("slash")
        , "backslash": K("backslash")
        , "sing": K("apostrophe")
        , "quote": K("dquote")
        , "(hyphen|hive)": K("hyphen")
        # operator
        , "(under | ska)": K("underscore")
        , "plus [<1to100>]": K("plus:%(1to100)d")
        , "minus [<1to100>]": K("minus:%(1to100)d")
        , "equal[s] [<1to100>]": K("equal:%(1to100)d")
        , "percent": K("percent")        
        , "dollar": K("dollar")
        , "(star | asterix | asterisk)": K("asterisk")
        , "hash [<1to100>]": K("hash:%(1to100)d")
        , "tilde": K("tilde")
        , "lat": T("@")
        , "(ampersand | amper)":K("ampersand")
        , "pipe": K("bar")
        # parenthesis
        , "laip": K("lparen")
        , "rape": K("rparen")
        , "lack": K("lbracket")
        , "rack": K("rbracket")
        , "lace": K("lbrace")
        , "race": K("rbrace")
        , "lang": T("<")
        , "rang": T(">")
        # operator combo
        , "greater than": T(" > ")
        , "less than": T(" < ")
        , "g-equal": T(" >= ")
        , "l-equal": T(" <= ")
        , "(triple arrow | tri-lang)": T(" <<< ")
        , "minus-equal": T(" -= ")
        , "plus-equal": T(" += ")
        , "star-equal": T(" *= ")
        , "minus-minus": T("--")
        , "plus-plus": T("++")
        , "double-equal": T(" == ")
        , "(not-equal | nequal)": T(" != ")
        , "logical-and": T(" && ")
        , "logical-or": T(" || ")
        , "left-shift": T(" << ")
        , "right-shift": T(" >> ")
        # space combo
        , "spive": T(" -")
        , "pive": T("- ")
        , "pivak": T("- [ ]")
        , "scol": T(": ")
        , "spipe": T(" | ")
        , "splus": T(" + ")
        , "spequal": T(" = ")
        , "scam": T(", ")
        , "shash": T("# ")
        , "lote": K("lparen,quote")
        # function keys
        , "F1 [key]": K("f1")
        , "F2 [key]": K("f2")
        , "F3 [key]": K("f3")
        , "F4 [key]": K("f4")
        , "F5 [key]": K("f5")
        , "F6 [key]": K("f6")
        , "F7 [key]": K("f7")
        , "F8 [key]": K("f8")
        , "F9 [key]": K("f9")
        , "F10 [key]": K("f10")
        , "F11 [key]": K("f11")
        , "F12 [key]": K("f12")
    }
    defaults = {
        "1to100":1
    }
    extras = [
        chc_base._1to100
    ]

class NavigatingKeysRule(MappingRule):
    mapping = {
        # Char
        "right [<1to100>]": K("right:%(1to100)d")
        , "left [<1to100>]": K("left:%(1to100)d")
        , "up [<1to100>]": K("up:%(1to100)d")
        , "down [<1to100>]": K("down:%(1to100)d")
        , "chuck [<1to100>]": K("delete:%(1to100)d")
        , "chook [<1to100>]": K("backspace:%(1to100)d")
        # Words
        , "foo [<1to100>]": K("c-right:%(1to100)d")
        , "sell foo [<1to100>]": K("sc-right:%(1to100)d")
        , "dee foo [<1to100>]": K("sc-right:%(1to100)d, backspace")
        , "bar [<1to100>]": K("c-left:%(1to100)d")
        , "sell bar [<1to100>]": K("sc-left:%(1to100)d")
        , "dee bar [<1to100>]": K("sc-left:%(1to100)d, backspace")
        , "sellword [<1to100>]": K("c-left") + K("sc-right:%(1to100)d")
        # Lines
        , "home": K("home")
        , "end": K("end")
        , "u-end": K("up,end")
        , "de-end": K("down,end")
        , "sellome": K("s-home")
        , "deelome": K("s-home, backspace")
        , "sellend": K("s-end")
        , "deelend": K("s-end, backspace")
        , "cleeline": K("home") + K("s-down:%(0to100)d") + K("s-end") + K("backspace:2,enter")
        , "selline [<0to100>]": K("home") + K("s-down:%(0to100)d") + K("s-end")
        , "deeline [<0to100>]": K("home") + K("s-down:%(0to100)d") + K("s-end") + K("backspace:2")
        , "coline [<0to100>]": K("home") + K("s-down:%(0to100)d") + K("s-end") + K("c-c")
        , "cutline [<0to100>]": K("home") + K("s-down:%(0to100)d") + K("s-end") + K("c-x")
        , "dupline  [<0to100>] [<1to10>]": K("home") + K("s-down:%(0to100)d") + K("s-end") + P("20") + K("c-c") + P("20") + K("enter") + K("c-v:%(1to10)d") # c-c needs to be isolated with medium pauses!!!
        # Line breaks
        , "eslap": K("end, enter")
        , "dotslap": K("end, dot, enter")
        , "camslap": K("end, comma, enter")
        , "semslap": K("end") + T(";") + K("enter")
        , "coalslap": K("end, colon, enter")
        , "altslap": K("a,enter")
        , "(downslap | deeslap)": K("down,enter")
        # Special line breaks
        , "slah (cam | cama)": K("end,enter") + T(", ")
        , "(slah amp | slamper)": K("end,enter") + T("& ")
        , "slah amp amp": K("end,enter") + T("&& ")
        , "slah pipe": K("end,enter") + T("| ")
        , "slah pipe pipe": K("end,enter") + T("|| ")
        , "slah plus": K("end,enter") + T("+ ")
        , "slah minus": K("end,enter") + T("- ")
        # Pages
        , "(page up | pup) [<1to100>]": K("pgup:%(1to100)d")
        , "(page down | poun) [<1to100>]": K("pgdown:%(1to100)d")
        , "go to home": K("c-home")
        , "go to end": K("c-end")
        , "sell-all": K("c-a")
    }
    defaults = {
        "0to100":1,
        "1to10":1,
        "1to100":1
    }
    extras = [
        chc_base._0to100,
        chc_base._1to10,
        chc_base._1to100
    ]

class ShortcutRule(MappingRule):
    mapping = {
        # general
        "quit [<1to100>]": K("escape:%(1to100)d")
        , "(cop | copy) [<1to100>]": K("c-c:%(1to100)d")
        , "cut [<1to100>]": K("c-x:%(1to100)d")
        , "paste [<1to100>]": K("c-v:%(1to100)d")
        , "(undo | scratch) [<1to100>]": K("c-z:%(1to100)d")
        , "redo [<1to100>]": K("c-y:%(1to100)d")
        , "find [<1to100>]": K("c-f:%(1to100)d")
        , "find now <text>": K("c-f") + T('%(text)s')
        , "close": K("c-w")
        # files
        , "(nuphyle | new file)": K("c-n")
        , "(ophyle |  open file)": K("c-o")
        , "(saphyle | save file)": K("c-s")
        , "(saphylas | save file as)": K("cs-s")
    }
    defaults = {
        "1to100":1,
        "text":""
    }
    extras = [
        chc_base.text,
        chc_base._1to100
    ]

class MetaKeysRule(MappingRule):
    mapping = {
        "<metakey> <letter_or_digit>": K("%(metakey)s-%(letter_or_digit)s")
        , "<metakey> <direction>": K("%(metakey)s-%(direction)s")
        , "winmove <direction> [<1to10>]": K("sw-%(direction)s:%(1to10)d")
        , "shift tab": K("s-tab")
        , "(metapoint | metadot)": K("a-dot")
        , "metaquote": K("a-quote")
        , "(alt slash | aslash)": K("a-slash")
        , "context": K("apps")
    }
    defaults = {
        "1to10":1,
        "text":""
    }
    extras = [
        chc_base.text,
        chc_base._1to10,
        chc_base.letter_or_digit,
        chc_base.direction,
        chc_base.metakey,
    ]

#---------------------------------------------------------------------------
# Dictation
#---------------------------------------------------------------------------

class DictationRule(MappingRule):
    exported = True
    mapping = dict(
        ("%s <text>"%k, (T(v)+T("%(text)s")))
        for k, v in chc_base.characters.items()
    )
    mapping.update(
        {
            "(space | ace) <text>": T(" %(text)s")
            , "<text> (space | ace)": T("%(text)s ")
            , "sing <text>": T("'%(text)s'")
            , "quote <text>": T('"%(text)s"')
            , "<text> spequals": T("%(text)s = ")
            , "<text> equals": T("%(text)s=")
            , "<text> coal": T("%(text)s:")
            , "<text> scol": T("%(text)s: ")
            , "<text> cam": T("%(text)s,")
            , "<text> scam": T("%(text)s, ")
        }
    )
    extras = [
        chc_base.text
    ]

# Format functions (by Tavis Rudd): Function name must start with "format_" and the Docstring defines the spoken-form.

def format_say(text):       
    """say <text>"""
    dictation = str(text)
    return dictation
    
def format_says(text):
    """says <text>"""
    dictation = str(text)
    return dictation + " "

def format_cap_say(text):
    """cap say <text>"""
    words = str(text).split(" ")
    return words[0].capitalize() + " ".join(w for w in words[1:])

def format_score(text):
    """score <text>"""
    words = [word.lower() for word in str(text).split(" ")]
    return "_".join(words)

def format_path(text):
    """path <text>"""
    dictation = str(text)
    if dictation.startswith("."):
        dictation = ". " + dictation[1:]
    return "/".join(dictation.split(" "))

def format_hyphen_word(text):
    """hi-word <text>"""
    dictation = str(text)
    return "-".join(dictation.split(" "))

def format_dot_word(text):
    """dot-word <text>"""
    dictation = str(text)
    return ".".join(dictation.split(" "))

def format_studley(text):
    """studley <text>"""
    words = [word.capitalize() for word in str(text).split(" ")]
    return "".join(words)

def format_camel(text):
    """camel <text>"""
    words = str(text).split(" ")
    return words[0] + "".join(w.capitalize() for w in words[1:])

def format_under_function(text):
    """under func <text>"""
    dictation = str(text)
    return "_".join(dictation.split(" ")) + "("

def format_studley_function(text):
    """studley func <text>"""
    dictation = str(text)
    words = [word.capitalize() for word in dictation.split(" ")]
    return "".join(words) + "("

def format_camel_function(text):
    """camel func <text>"""
    dictation = str(text)
    return "_".join(dictation.split(" ")) + "("

def format_one_word(text):
    """one word <text>"""
    dictation = str(text)
    return "".join(dictation.split(" "))

def format_upper_one_word(text):
    """[one word] upper <text>"""
    dictation = str(text)
    words = [word.upper() for word in dictation.split(" ")]
    return "".join(words)

def format_lower_one_word(text):
    """[one word] lower <text>"""
    dictation = str(text)
    words = [word.lower() for word in dictation.split(" ")]
    return "".join(words)

def format_upper_score(text):
    """upper score <text>"""
    dictation = str(text)
    words = [word.upper() for word in dictation.split(" ")]
    return "_".join(words)

format_functions = {
#    "jive <dictation>": run('(dss/clojure-join-words "%(dictation)s")')
#    , "keyword <dictation>": run('(dss/clojure-insert-keyword "%(dictation)s")')
    }

for name, function in locals().items():
    if name.startswith("format_") and callable(function):
        spoken_form = function.__doc__.strip()
        def wrap_function(function):
            def _function(text):
                T(function(text)).execute()
            return Function(_function)
        format_functions[spoken_form] = wrap_function(function)

class FormattedDictationRule(MappingRule):
    exported = True
    mapping = format_functions
    extras = [
        chc_base.text
    ]

#---------------------------------------------------------------------------
# Text
#---------------------------------------------------------------------------

class PhraseRule(MappingRule):
    mapping = {
        "(filex | phaix) <file_extension>": T("%(file_extension)s")
        , "to do [<text>]": T("TODO: %(text)s")
    }
    defaults = {
        "text":""
    }
    extras = [
        chc_base.text,
        chc_base.file_extension
    ]
    
#---------------------------------------------------------------------------
# OS specific
#---------------------------------------------------------------------------

class WindowsRule(MappingRule):
    mapping = {
        #, "closapp": K("win:down, a-f4, win:up") # switch
        #, "closapp": K("alt:down, f4, alt:up")
        #, "closapp": K("a-f4")
        "closapp": Function(lambda: natlink.recognitionMimic(["close", "window"]))
        #, "swatch": K("alt:down") + P("20") + K("tab") + P("20") + K("alt:up") # switch app
        #, "swatch": K("win:down, a-tab, win:up") # switch tab 
        , "swatch": StartApp("explorer.exe", chc_base.dir_bin + "window-switch.lnk")
        , "swatcha": StartApp("explorer.exe", chc_base.dir_bin + "window-switch.lnk") + K("enter")
        , "swap": K("c-tab") # switch tab
        , "putty <host_name>": DynStartApp(chc_base.exe_putty, "-load", "%(host_name)s")
        , "sound settings": WinCmd("C:\Windows\System32\mmsys.cpl")
    }
    extras = [
        chc_base.host_name
    ]

#---------------------------------------------------------------------------
# Dragon
#---------------------------------------------------------------------------

class DragonRule(MappingRule):
    mapping = {
        "(go-to-sleep | snore | mic-sleep)": Function(lambda: natlink.setMicState("sleeping"))
        , "(lock-Dragon|turn-mic-off)": Function(lambda: natlink.setMicState("off"))
        , "german profile": Function(lambda: natlink.saveUser() + natlink.openUser("Codebold german"))
        , "englisches Profil": Function(lambda: natlink.saveUser() + natlink.openUser("Codebold"))
        , "reload grammar[s]": Function(lambda: updateAllGrammars())
        , "reload <grammar>": GrammarUpdate()
        , "como": Function(lambda: natlink.recognitionMimic(["switch", "to", "command", "mode"]))
        , "diemo": Function(lambda: natlink.recognitionMimic(["start", "dictation", "mode"]))
        , "nomo": Function(lambda: natlink.recognitionMimic(["normal", "mode", "on"]))
        , "sleemo": Function(lambda: natlink.recognitionMimic(["go", "to", "sleep"]))
        , "dictation": Function(lambda: natlink.recognitionMimic(["show", "dictation", "box"]))
        , "dictox": Function(lambda: natlink.recognitionMimic(["normal", "mode", "on"])) + Function(lambda: natlink.recognitionMimic(["show", "dictation", "box"]))
        , "transfox": Function(lambda: natlink.recognitionMimic(["click", "transfer"])) + Function(lambda: natlink.recognitionMimic(["command", "mode", "on"]))
        , "blitz NatLink": Function(blitz_natlink_status)
        , "show NatLink": Function(show_natlink_status)
    }
    extras = [
        chc_base.grammar
    ]


