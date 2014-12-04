import string

from dragonfly import (
    Choice,
    Dictation,
    IntegerRef,
    NumberRef,
)

from util.choices import (
    combine_choices,
    parse_user_choices
)

#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------

dir_bin = "C:\\Python\\NatLink\NatLink\\MacroSystem\\bin\\"
exe_putty = "C:\Program Files (x86)\PuTTY\putty.exe"

#---------------------------------------------------------------------------
# Dictations
#---------------------------------------------------------------------------

text = Dictation("text")
text1 = Dictation("text1")
text2 = Dictation("text2")
text3 = Dictation("text3")

#---------------------------------------------------------------------------
# Numbers
#---------------------------------------------------------------------------

any_number_n = NumberRef("n")
any_number_m = NumberRef("m")
any_number_o = NumberRef("o")
_1to10 = IntegerRef("1to10", 1, 11)
_1to100 = IntegerRef("1to100", 1, 101)
_1to1000 = IntegerRef("1to1000", 1, 1001)
_1to10000 = IntegerRef("1to10000", 1, 10001)
_0to12 = IntegerRef("0to12", 0, 13)
_0to60 = IntegerRef("0to60", 0, 60)
_0to10 = IntegerRef("0to10", 0, 11)
_0to100 = IntegerRef("0to100", 0, 101)
_0to1000 = IntegerRef("0to1000", 0, 1001)
_0to10000 = IntegerRef("0to10000", 0, 10001)

#---------------------------------------------------------------------------
# Digits
#---------------------------------------------------------------------------

digits = dict((word, str(i))
              for (i, word) in
              enumerate("zero one two three four five six seven eight nine".split()))
digit = Choice("digit", digits)

#---------------------------------------------------------------------------
# Letters
#---------------------------------------------------------------------------

# Alpha Alf
# Bravo Brav
# Charlie Coy
# Delta Doy
# Echo Eck
# Foxtrot Foy
# Golf Goy Gee
# Hotel Hote Hoop
# India Ing Iish
# Juliet Joy
# Kilo Keel
# Lima Loy Lee
# Mike Moy
# November Nancy Noy
# Oscar Osc
# Papa Poy
# Quebec Queen
# Romeo Rome
# Sierra Soi
# Tango Toi
# Uniform Uni
# Victor Vick
# Whiskey Whesk
# X-ray Xanth
# Yankee Yoi
# Zulu Zul

alpha_words = [word for word in
               """
               Aff Brav Cheak Doy Emo Fay Goff Hoop Ish Jo Keel Lee Mike Noy Osh Pui Queen Ree Soi Tay Uni Van Wes Xenon Yaa Zul """.split() if word]
alpha_word = Choice("alpha_word", dict((w, w[0].lower()) for w in alpha_words))

letters = dict([(l.upper()+'.', l) for l in string.letters[:26]]
                   + [(w, w[0].lower()) for w in alpha_words])
letter = Choice("letter", letters)

letter_or_digit = Choice(
    "letter_or_digit",
    combine_choices(letter, digit))

#---------------------------------------------------------------------------
# Characters
#---------------------------------------------------------------------------

characters = {
    "quote":'"'
    , "(sing | single quote)":"'"
    , "(colon|coal)":":"
    , "(semi colon|sem-col|sem-coal)":";"
    , "tilde":"~"
    , "(ampersand | amper)":"&"
    , "laip":"("
    , "rape":")"
    , "lace":"{"
    , "race":"}"
    , "lack":"["
    , "rack":"]"
    , "(hyphen | hive)":"-"
    , "(space | spa | paa)":" "
    , "(under[score] | score)":"_"
    , "slash":"/"
    , "backslash":"\\"
    , "cam":","
    , "(dot|period)":"."
    , "hash":"#"
    , "dollar":"$"
    , "percent":"%"
    , "clam":"!"
    , "quest[ion]":"?"
    , "star":"*"
    , "plus":"+"
    , "pipe":"|"
    , "lat":"@"
    , "equal[s]":"="
    , "(greater than | rang)":">"
    , "(less than | lang)":"<"
}
character = Choice("character", characters)

letter_or_character = Choice(
    "letter_or_character",
    combine_choices(letter, character))

simple_character = Choice(
    "simple_character",
    combine_choices(alpha_word, character))

full_character = Choice(
    "full_character_choices",
    combine_choices(letter_or_character, digit))

#---------------------------------------------------------------------------
# Keyboard keys
#---------------------------------------------------------------------------

metakeys = {
    "alt":"a"
    , "control":"c"
    , "shift":"s"
    , "Windows":"w"
}
metakey = Choice("metakey", metakeys)

#---------------------------------------------------------------------------
# Major system codes
#---------------------------------------------------------------------------

major_system_codes = dict((word.strip(), i)
         for i, word in enumerate("""
         saw    tie   knee  emu   ear   eel    shoe  cow  ivy   bee
         toes   tit   teen  dime  tire  tile   dish  duck dove  tub
         nose   nut   nun   name  Nero  nail   notch neck knive knob
         mouse  mat   moon  mummy moor  mule   mojo  moko movie map
         rose   rat   rain  ram   rear  rail   rush  rock roof  rope
         laze   light lion  lamb  lure  lily   leash log  leaf  lab
         cheese sheet chain chum  chair jail   judge jock chief ship
         kiss   kit   coin  comb  car   collie case  cock cave  cab
         face   vat   fan   foam  fire  file   fish  fog  fife  fab
         base   bat   bin   bam   bar   bell   beach pug  beef babe
         """.split()))
major_system_code = Choice("major_system_code", major_system_codes)

#---------------------------------------------------------------------------
# Directions
#---------------------------------------------------------------------------

directions = dict((w, w) for w in "up right down left".split())
direction = Choice("direction", directions)

backwards = dict((w, w) for w in "up back backward left".split())
backward = Choice("backward", backwards)

forwards = dict((w, w) for w in "down forward right".split())
forward = Choice("forward", forwards)

columns = dict((w, w) for w in "column col call".split())
column = Choice("column", columns)

#---------------------------------------------------------------------------
# Time
#---------------------------------------------------------------------------

time_periods = {
    "AM": "am"
    , "cap AM":"AM"
    , "PM": "pm"
    , "cap PM": "PM"
}
time_period = Choice("time_period", time_periods)

#---------------------------------------------------------------------------
# Code elements
#---------------------------------------------------------------------------

functions = dict((w, w) for w in "func def function".split())
function = Choice("function", functions)

operators = {
    "equals":"="
    , "plus":"+"
    , "minus":"-"
    , "star":"*"
    , "slash":"/"
    , "power":"^"
}
operator = Choice("operator", operators)

#---------------------------------------------------------------------------
# Grammars
#---------------------------------------------------------------------------

grammars = {
    "base":"_base.py"
    , "other[s]":"_others.py"
}
grammar = Choice("grammar", grammars)

#---------------------------------------------------------------------------
# Files and folders
#---------------------------------------------------------------------------

common_files = {
    "emacs config":"~/.emacs.d/init.el"
    , "emacs alias":"~/.emacs.d/eshell/alias"
    , "emacs dictionary":"~/.emacs.d/dict/dict"
}
user_common_files = parse_user_choices("common_files.txt")
common_file = Choice("common_file", combine_choices(common_files, user_common_files))

common_folders = {
    "home":'~/'
    , "desktop":"~/Desktop/"
    , "downloads":"~/Downloads/"
    , "emacs":'~/.emacs.d/'
    , "C":'c:/'
    , "macros":'c:/Python/NatLink/NatLink/MacroSystem/'
    , "rules":'c:/Python/NatLink/NatLink/MacroSystem/rules/'
    , "actions":'c:/Python/NatLink/NatLink/MacroSystem/actions/'
    , "dragonfly":'C:\Python\DragonFly\dragonfly\dragonfly'
    , "root":'/root/'
    , "conf":"/etc/"
    , "conf apache":"/etc/apache2/"
    , "conf postfix":"/etc/postfix/"
    , "web":"/var/www/"
    , "zimbra":"/opt/zimbra/"
}
user_common_folders = parse_user_choices("common_folders.txt")
common_folder = Choice("common_folder", combine_choices(common_folders, user_common_folders))

file_extensions = {
    "CSS":".css"
    , "cert":".crt"
    , "config[uration]":".conf"
    , "Emacs":".el"
    , "G zip":".gz"
    , "HTML":".html"
    , "key":".key"
    , "MD 5":".md5"
    , "Java":".java"
    , "Java archive":".jar"
    , "JavaScript":".js"
    , "JPEG":".jpg"
    , "PNG":".png"
    , "Python":".py"
    , "Python (c | compiled)":".pyc"
    , "Python library":".pyd"
    , "shell":".sh"
    , "tar":".tar"
    , "tex":".tex"
    , "text":".txt"
    , "XML":".xml"
    , "zip":".zip"
}
user_file_extensions = parse_user_choices("file_extensions.txt")
file_extension = Choice("file_extension", combine_choices(file_extensions, user_file_extensions))

#---------------------------------------------------------------------------
# Host and user names
#---------------------------------------------------------------------------

host_names = {
    "(localhost | local)":"localhost"
}
user_host_names = parse_user_choices("host_names.txt")
host_name = Choice("host_name", combine_choices(host_names, user_host_names))

os_users = {
    "root":"root"
    , "daemon":"daemon"
    , "sys":"sys"
    , "sync":"sync"
    , "man":"man"
    , "mail":"mail"
    , "news":"news"
    , "proxy":"proxy"
    , "backup":"backup"
    , "list":"list"
    , "nobody":"nobody"
    , "whoopsie":"whoopsie"
    , "gnats":"gnats"
    , "sys log":"syslog"
    , "sudo":"sudo"
    , "SSH":"sshd"
    , "NTP":"ntp"
    , "postfix":"postfix"
    , "postgres":"postgres"
    , "MySQL":"mysql"
    , "red mine":"redmine"
    , "git":"git"
    , "zimbra":"zimbra"
    , "apache":"www-data"
    , "me":"me"
    , "you":"you"
}
user_os_users = parse_user_choices("os_users.txt")
os_user = Choice("os_user", combine_choices(os_users, user_os_users))

#---------------------------------------------------------------------------
# Protocols
#---------------------------------------------------------------------------

protocols = {
    "FTP":"ftp://"
    , "git":"git://"
    , "HTTP":"http://"
    , "HTTPS":"https://"
    , "SS H":"ssh://"
}
user_protocols = parse_user_choices("protocols.txt")
protocol = Choice("protocol", combine_choices(protocols, user_protocols))

#---------------------------------------------------------------------------
# Command line tools
#---------------------------------------------------------------------------

greps = {
    "grep":"grep"
    , "(a | approx | approximate) grep":"agrep"
    , "(e | ex | extended) grep":"egrep"
    , "(f | fast) grep":"fgrep"
}
grep = Choice("grep", greps)

#---------------------------------------------------------------------------
# Websites
#---------------------------------------------------------------------------

websites = {
    "Wikipedia":"http://wikipedia.org/"
    , "Google":"https://google.com/"
    , "Facebook":"https://facebook.com/"
}
user_websites = parse_user_choices("websites.txt")
website = Choice("website", combine_choices(websites, user_websites))
