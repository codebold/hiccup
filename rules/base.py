import choices.base as chc_base
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

from actions.action_dynstartapp import (
    DynStartApp
)

from util import (
    K,
    T,
    P,
    updateGrammar,
    updateAllGrammars,
    GrammarUpdate,
    windows,
    blitz_natlink_status,
    show_natlink_status
)

from subprocess import (
    call
)

#---------------------------------------------------------------------------
# Characters
#---------------------------------------------------------------------------
class AlphaRule(MappingRule):
    mapping = {}
    for word in chc_base.alpha_words:
        letter = word[0].lower()
        mapping[word] = K(letter)
        mapping['cap ' +word] = K(letter.upper())
        mapping['insert ' +word] = T(word.lower())

class LetterSeqRule(CompoundRule):
    spec = "(letters|spell) <letter_sequence>"
    extras = [Repetition(chc_base.letter,
                         min=1, max=26,
                         name="letter_sequence")]

    def _process_recognition(self, node, extras):
        for letter in extras["letter_sequence"]:
            T(letter).execute()

class CharRule(MappingRule):
    # this is part of the main sequence command, and doesn't need exporting
    # exported = False
    mapping = {
        "(space | ace | paa)": K("space")
        , "paa paa": K("space:2")
        , "(colon|coal)": K("colon")
        , "(semi colon|sem-col|sem-coal)": T(";")
        , "(hyphen|hive)": K("hyphen")
        , "tilde": K("tilde")
        , "percent": K("percent")
        , "(ampersand | amper)":K("ampersand")
        # parenthesis
        , "laip": K("lparen")
        , "rape": K("rparen")
        , "lack": K("lbracket")
        , "rack": K("rbracket")
        , "lace": K("lbrace")
        , "race": K("rbrace")

        , "slash": K("slash")
        , "backslash": K("backslash")
        , "pipe": K("bar")
        , "(comma | cam)": K("comma")
        , "scam": T(", ")
        , "(under | ska)": K("underscore")
        , "quote": K("dquote")
        , "sing": K("apostrophe")

        , "double quote": K("dquote:2")
        , "(dot | period)": K("dot")
        , "dot dot": K("dot:2")
        , "dot dot dot": K("dot:3")
        , "equal[s]": K("equal")
        , "hash": K("hash")
        , "shash": T("# ")
        , "plus": K("plus")
        , "minus": K("minus")
        , "dollar": K("dollar")
        , "(exclaim|clam)": K("exclamation")
        , "(question-mark|quest)": K("question")
        , "(star | asterix | asterisk)": K("asterisk")

        , "rang": T(">")
        , "greater than": T(" > ")
        , "lang": T("<")
        , "(triple arrow | tri-lang)": T(" <<< ")
        , "less than": T(" < ")
        , "lat": T("@")

        , "g-equal": T(" >= ")
        , "l-equal": T(" <= ")
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

        , "spive": T(" -")
        , "pive": T("- ")
        , "pivak": T("- [ ]")
        , "scol": T(": ")
        , "spipe": T(" | ")
        , "splus": T(" + ")
        , "spequal": T(" = ")
        , "cama": T(", ")
        , "equal-scol": T("=: ")
        , "equote":K("equal,quote,quote,left")
        #, "dolaip": (T("$()") + K("left"))
        , "clap": K("colon,enter")
        , "lote": K("lparen,quote")
        , "lace-quote": K("lparen,right,colon,quote")
        
        , "slah (cam | cama)": (K("end,enter") + T(", "))
        , "(slah amp | slamper)": (K("end,enter") + T("& "))
        , "slah amp amp": (K("end,enter") + T("&& "))
        , "slah pipe": (K("end,enter") + T("| "))
        , "slah pipe pipe": (K("end,enter") + T("|| "))
        , "slah plus": (K("end,enter") + T("+ "))
        , "slah minus": (K("end,enter") + T("- "))
    }

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
# Navigating
#---------------------------------------------------------------------------

class DragoflyRule(MappingRule):
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

class WindowsRule(MappingRule):
    mapping = {
        "context": K("apps")
        
        #, "closapp": K("win:down, a-f4, win:up") # switch
        #, "closapp": K("alt:down, f4, alt:up")
        #, "closapp": K("a-f4")
        , "closapp": Function(lambda: natlink.recognitionMimic(["close", "window"]))
        #, "swatch": K("alt:down") + P("20") + K("tab") + P("20") + K("alt:up") # switch app
        #, "swatch": K("win:down, a-tab, win:up") # switch tab 
        , "swatch": StartApp("explorer.exe", chc_base.dir_bin + "window-switch.lnk")
        , "swatcha": StartApp("explorer.exe", chc_base.dir_bin + "window-switch.lnk") + K("enter")
        , "sound settings": StartApp("explorer.exe", chc_base.dir_bin + "Sound.lnk")
        , "swap": K("c-tab") # switch tab
        , "putty <host_name>": DynStartApp(chc_base.exe_putty, "-load", "%(host_name)s")
    }
    extras = [
        chc_base.host_name
    ]

class FindRule(MappingRule):
    mapping = {
        # general
        "find": K("enter")
}

class KeyboardRule(MappingRule):
    mapping = {
        # general
        "(quit | escape) [<1to100>]": K("escape:%(1to100)d")
        , "quit quit": K("escape:2")
        , "quit quit quit": K("escape:3")
        , "(cop | copy)": K("c-c")
        , "cut": K("c-x")
        , "paste [<1to100>]": K("c-v:%(1to100)d")
        , "paste paste": K("c-v:2")
        , "paste paste paste": K("c-v:3")
        , "(undo | scratch) [<1to100>]": K("c-z:%(1to100)d")
        , "(undo undo | scratch scratch)": K("c-z:2")
        , "(undo undo undo | scratch scratch scratch)": K("c-z:%3")
        , "redo [<1to100>]": K("c-y:%(1to100)d")
        , "redo redo": K("c-y:2")
        , "redo redo redo": K("c-y:3")
        , "find [<1to100>]": K("c-f:%(1to100)d")
        , "find find": K("c-f:2")
        , "find find find": K("c-f:3")
        , "find now <text>": K("c-f") + T('%(text)s')
        # files
        , "new file": K("c-n")
        , "o-file": K("c-o")
        , "sa-file": K("c-s")
        , "sa-file-as": K("cs-s")
        , "close": K("c-w")
        , "(filex | phaix) <file_extension>": T("%(file_extension)s")
        , "to do [<text>]": T("TODO: %(text)s")
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
        # Char
        , "right [<1to100>]": K("right:%(1to100)d")
        , "right right": K("right:2")
        , "right right right": K("right:3")
        , "left [<1to100>]": K("left:%(1to100)d")
        , "left left": K("left:2")
        , "left left left": K("left:3")
        , "up [<1to100>]": K("up:%(1to100)d")
        , "up up": K("up:2")
        , "up up up": K("up:3")
        , "down [<1to100>]": K("down:%(1to100)d")
        , "down down": K("down:2")
        , "down down down": K("down:3")
        , "chuck [<1to100>]": K("delete:%(1to100)d")
        , "chuck chuck": K("delete:2")
        , "chuck chuck chuck": K("delete:3")
        , "(chook | backspace) [<1to100>]": K("backspace:%(1to100)d")
        , "chook chook": K("backspace:2")
        , "chook chook chook": K("backspace:3")
        # Words
        , "(forward | foo) [<1to100>]": K("c-right:%(1to100)d")
        , "foo foo": K("c-right:2")
        , "foo foo foo": K("c-right:3")
        , "sell foo [<1to100>]": K("sc-right:%(1to100)d")
        , "dee foo [<1to100>]": K("sc-right:%(1to100)d, backspace")
        , "(backward | bar) [<1to100>]": K("c-left:%(1to100)d")
        , "bar bar": K("c-left:2")
        , "bar bar bar": K("c-left:3")
        , "sell bar [<1to100>]": K("sc-left:%(1to100)d")
        , "dee bar [<1to100>]": K("sc-left:%(1to100)d, backspace")
        , "sellword [<1to100>]": K("c-left") + K("sc-right:%(1to100)d")
        , "sell-all": K("c-a")
        # Lines
        , "slap [<1to100>]": K("enter:%(1to100)d")
        , "slap slap": K("enter:2")
        , "slap slap slap": K("enter:3")
        , "eslap": K("end, enter")
        , "dotslap": K("end, dot, enter")
        , "camslap": K("end, comma, enter")
        , "semslap": K("end") + T(";") + K("enter")
        , "coalslap": K("end, colon, enter")
        , "altslap": K("a,enter")
        , "(downslap | deeslap)": K("down,enter")
        , "(tap | tab) [<1to100>]": K("tab:%(1to100)d")
        , "tab tab": K("tab:2")
        , "tab tab tab": K("tab:3")
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
        , "dupline  [<0to100>] [<1to10>]": K("home") + K("s-down:%(0to100)d") + K("s-end") + P("20") + K("c-c") + P("20") + K("enter") + K("c-v:%(1to10)d") # c-c needs to be isolated with medium pauses!!!
        # Pages
        , "(page up | pup) [<1to100>]": K("pgup:%(1to100)d")
        , "pup pup": K("pgup:2")
        , "pup pup pup": K("pgup:3")
        , "(page down | poun) [<1to100>]": K("pgdown:%(1to100)d")
        , "poun poun": K("pgdown:2")
        , "poun poun poun": K("pgdown:3")
        , "go to home": K("c-home")
        , "go to end": K("c-end")
        ## special key sequences
        , "<metakey> <letter_or_digit>": K("%(metakey)s-%(letter_or_digit)s")
        , "<metakey> <direction>": K("%(metakey)s-%(direction)s")
        , "winmove <direction> [<1to10>]": K("sw-%(direction)s:%(1to10)d")
        , "shift tab": K("s-tab")
        , "(metapoint | metadot)": K("a-dot")
        , "metaquote": K("a-quote")
        , "(alt slash | aslash)": K("a-slash")
        , "escape": K("escape")
    }
    defaults = {
        "0to100":0,
        "1to100":1,
        "0to10":0,
        "1to10":1,
        "text":""
    }
    extras = [
        chc_base.text,
        chc_base._0to10,
        chc_base._0to100,
        chc_base._1to10,
        chc_base._1to100,
        chc_base.letter_or_digit,
        chc_base.direction,
        chc_base.metakey,
        chc_base.file_extension
    ]

#---------------------------------------------------------------------------
# Formatted dictation
#---------------------------------------------------------------------------

def format_say(text):       # Function name must start with "format_".
    """say <text>"""        # Docstring defining spoken-form.
    dictation = str(text)        # Get written-form of dictated dictation.
    return dictation                  # Put underscores between words.
    
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
# Character Dictation
#---------------------------------------------------------------------------
    
class CharacterDictationRule(MappingRule):
    exported = True
    mapping = dict(
        ("%s <text>"%k, (T(v)+T("%(text)s")))
        for k, v in chc_base.characters.items()
    )
    mapping.update(
        {
            "space <text>": T(" %(text)s")
            , "<text> space": T("%(text)s ")
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
        chc_base.text,
        chc_base.character
    ]
# TODO: Check if here only charaterS is needed

    
#---------------------------------------------------------------------------
# Repeat
#---------------------------------------------------------------------------

def _create_main_sequence():
    alternatives = [
        RuleRef(rule=AlphaRule())
        , RuleRef(rule=CharRule())
        , RuleRef(rule=LetterSeqRule())
        , RuleRef(rule=LiteralRule())
        , RuleRef(rule=KeyboardRule())
    ]
    # adding too many rules doesn't work because the grammar becomes
    # too complex for natlink to recognize it. It's also sensitive
    # to the maximum number of repetitions

    return Repetition(Alternative(alternatives),
                      min=1, max=6,     # barfs at >7
                      name="sequence")

class RepeatRule(CompoundRule):
    spec = "[<reps>] <sequence> [then]"
    extras = [_create_main_sequence(), IntegerRef("reps", 1, 100)]
    defaults = {"reps": 1}

    def _process_recognition(self, node, extras):
        sequence = extras["sequence"]
        count = extras["reps"]
        for i in range(count):
            for action in sequence:
                action.execute()
