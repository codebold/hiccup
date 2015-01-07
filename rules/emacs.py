from dragonfly import MappingRule

from actions.action_application import Emacs
from actions.action_shortcut import (
    K,
    T,
    P
)

import choices.base as chc_base

#---------------------------------------------------------------------------
# Keyboard
#---------------------------------------------------------------------------

class EmacsNavigatingKeysRule(MappingRule):
    mapping = {
        # Words
        "foo [<1to100>]": Emacs("forward-word:%(1to100)d")
        , "sell foo [<1to100>]": K("sc-right:%(1to100)d")
        , "dee foo [<1to100>]": K("sc-right:%(1to100)d, backspace")
        , "bar [<1to100>]": Emacs("backward-word:%(1to100)d")
        , "sell bar [<1to100>]": K("sc-left:%(1to100)d")
        , "dee bar [<1to100>]": K("sc-left:%(1to100)d, backspace")
        , "sellword [<1to100>]": K("c-left") + K("sc-right:%(1to100)d")
        # Lines
        , "home": Emacs("move-beginning-of-line")
        , "end": Emacs("move-end-of-line")
        , "u-end": K("up") + Emacs("move-end-of-line")
        , "de-end": K("down") + Emacs("move-end-of-line")
        , "sellome": K("s-home")
        , "deelome": K("s-home, backspace")
        , "sellend": K("s-end")
        , "deelend": K("s-end, backspace")
        , "cleeline": K("home") + K("s-down:%(0to100)d") + K("s-end") + K("backspace:2,enter")
        , "selline [<0to100>]": K("home") + K("s-down:%(0to100)d") + K("s-end")
        , "deeline [<0to100>]": K("home") + K("s-down:%(0to100)d") + K("s-end") + K("backspace:2")
        , "coline [<0to100>]": K("home") + K("s-down:%(0to100)d") + K("s-end") + K("c-c")
        , "dupline  [<0to100>] [<1to10>]": K("home") + K("s-down:%(0to100)d") + K("s-end") + P("20") + K("c-c") + P("20") + K("enter") + K("c-v:%(1to10)d") # c-c needs to be isolated with medium pauses!!!
        # Line breaks
        , "eslap": Emacs("move-end-of-line") + K("enter")
        , "dotslap": Emacs("move-end-of-line") + K("dot, enter")
        , "camslap": Emacs("move-end-of-line") + K("comma, enter")
        , "semslap": Emacs("move-end-of-line") + T(";") + K("enter")
        , "coalslap": Emacs("move-end-of-line") + K("colon, enter")
        # Special line breaks
        , "slah (cam | cama)": Emacs("move-end-of-line") + K("enter") + T(", ")
        , "(slah amp | slamper)": Emacs("move-end-of-line") + K("enter") + T("& ")
        , "slah amp amp": Emacs("move-end-of-line") + K("enter") + T("&& ")
        , "slah pipe": Emacs("move-end-of-line") + K("enter") + T("| ")
        , "slah pipe pipe": Emacs("move-end-of-line") + K("enter") + T("|| ")
        , "slah plus": Emacs("move-end-of-line") + K("enter") + T("+ ")
        , "slah minus": Emacs("move-end-of-line") + K("enter") + T("- ")
        # Pages
        , "go to home": Emacs("beginning-of-buffer")
        , "go to end": Emacs("end-of-buffer")
        , "sell-all": Emacs("mark-whole-buffer")
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

class EmacsShortcutRule(MappingRule):
    mapping = {
        "quit [<1to100>]": K("c-g:%(1to100)d")
        , "(cop | copy)": Emacs("clipboard-kill-ring-save")
        , "cut": Emacs("clipboard-kill-region")
        , "paste": Emacs("clipboard-yank")        
    }
    defaults = {
        "1to100":1
    }
    extras = [
        chc_base._1to100
    ]

#---------------------------------------------------------------------------
# Core Rule
#---------------------------------------------------------------------------

class EmacsCoreRule(MappingRule):
    mapping = {
        "command": K("a-u")
        , "elast": Emacs("eval-print-last-sexp")
        , "close emacs": Emacs("save-buffers-kill-terminal")
        , "(eshell | shell) [<1to10>]": K("c-%(1to10)s") + Emacs("eshell")
        ## bindings
        , "describe function": Emacs("describe-function")
        , "describe key": Emacs("describe-key")
        ## chars
        , "unicode": Emacs("insert-char")
        , "transpose-chars": Emacs("transpose-chars")
        ## words
        , "transpose-words":  Emacs("transpose-words")
        , "replace word [with] <text>": Emacs("kill-word") + T("%(text)s")
        , "replace last word [with] <text>": Emacs("backward-word") + Emacs("kill-word") + T("%(text)s")
        , "(downcase word | down-word)": Emacs("downcase-word")
        , "downcase last": Emacs("(downcase-word -1)")
        , "(upcase word | up-word)": Emacs("upcase-word")
        , "upcase last": Emacs("(upcase-word -1)")
        , "(capitalize | cap) word": Emacs("capitalize-word")
        , "cap last [word]": Emacs("(capitalize-word -1)")
        , "sub-word-mode": Emacs("subword-mode")
        ## lines
        , "sort-lines": Emacs("sort-lines")
        , "(transpose-lines | trans-lines)": Emacs("transpose-lines")
        , "sort-columns": Emacs("sort-columns")
        , "flush-lines": Emacs("flush-lines")
        , "keep-lines": Emacs("keep-lines")
        , "align-regexp": Emacs("align-regexp")
        , "selline <0to10000> to <1to10000>": Emacs("goto-line") + T("%(0to10000)d\n") + K("home") + Emacs("set-mark-command") + Emacs("goto-line") + T("%(1to10000)d\n") + K("end")
#        , "open-line [<1to10>]": Emacs("dss/-open-line-indent", narg='1to10')
#        , "(o-line | jab)": Emacs("dss/smart-open-line")
        , "count lines": Emacs("count-lines-region")
        , "count lines page": Emacs("count-lines-page")
        ## registers
        , "ropy <letter_or_digit>": Emacs("copy-to-register") + T("%(letter_or_digit)s")
        , "repend <letter_or_digit>": Emacs("prepend-to-register") + T("%(letter_or_digit)s")
        , "rapend <letter_or_digit>": Emacs("append-to-register") + T("%(letter_or_digit)s")
        , "raste <letter_or_digit>": Emacs("insert-register") + T("%(letter_or_digit)s")
        , "roint <letter_or_digit>": Emacs("point-to-register") + T("%(letter_or_digit)s")
        , "reroint <letter_or_digit>": Emacs("register-to-point") + T("%(letter_or_digit)s")
        , "rump <letter_or_digit>": Emacs("jump-to-register") + T("%(letter_or_digit)s")
        , "rump": Emacs("jump-to-register")
        , "rist": Emacs("list-registers")
        , "rindow[s] <letter_or_digit>": Emacs("window-configuration-to-register") + T("%(letter_or_digit)s")
        , "rame[s] <letter_or_digit>": Emacs("frame-configuration-to-register") + K("%(letter_or_digit)s")
        , "ruffer": Emacs("undo-tree-save-state-to-register")
        , "reruffer": Emacs("undo-tree-restore-state-to-register")
        ## mark
        , "[set] mark": Emacs("set-mark-command")
        , "sell up": Emacs("set-mark-command") + K("up")
        , "sell down": Emacs("set-mark-command") + K("down")
        , "point mark": Emacs("set-mark-command") + Emacs("set-mark-command")
        , "visible-marks": Emacs("visible-mark-mode")
        , "swap mark": Emacs("exchange-point-and-mark")
        , "jump mark": Emacs("pop-to-mark-command")
        , "glo[bal]-jark": Emacs("pop-global-mark")
        #, "(toggle mark | mark off | tark)": Emacs("k2-toggle-mark")
        #, sharks
        , "highline mode": Emacs("hl-line-mode")
        ## operations on special markers
        #, "skack": Emacs("(dss/skeleton-next-position t)")
        #, "skext": Emacs("dss/skeleton-next-position")
        ## region
        , "(capitalize|cap) [(region | it)]": Emacs("capitalize-region")
        , "downcase [(region | it)]": Emacs("downcase-region")
        , "upcase [(region | it)]": Emacs("upcase-region")
        #, "quote-(region | it)": Emacs("dss/quote-region")
        #, "stud-(region | it)": Emacs("dss/words-studley-region")
        #, "jive-stud-(region | it)": Emacs("dss/words-studley-to-sep-region")
        #, "single-quote-region": Emacs("dss/single-quote-region")
        #, "(eval | evaluate) region": Emacs("eval-region")
        , "flash-region": Emacs("dss/flash-region")
        , "indent-region": Emacs("indent-region")
        , "narrow-to-region": Emacs("narrow-to-region")
        , "widen-to-buffer": Emacs("widen-to-buffer")
        #  the following two commands assume that the region has the
        #  point at the top and the mark at the bottom
        #, "shrink-region [<1to10>]": K(
        #    "right:%(1to10)d,c-x,c-x,left:%(1to10)d,c-x,c-x")
        #, "shrink-region by <1to10> line[s]": K(
        #    "down:%(1to10)d,c-x,c-x,up:%(1to10)d,c-x,c-x")
        ## kill ring
        , "kill-ring": Emacs("browse-kill-ring")
        # goto
        , "goost": Emacs("goto-last-change")
        , "em-goost": Emacs("goto-last-change-with-auto-marks")
        , "line <1to10000>": Emacs("goto-line") + T("%(1to10000)d\n") + Emacs("back-to-indentation")        
        ## movement
        , "snap": Emacs("back-to-indentation")
        , "de-snap": K("down") + Emacs("back-to-indentation")
        , "u-snap": K("up") + Emacs("back-to-indentation")
        #, "snap <0to1000>": (
        #    Emacs("dss/local-line-jump")
        #    + T("%(0to1000)s\n"))
        #, "(eol | yall | y'all) <0to1000>": (
        #    Emacs("dss/local-line-jump") +
        #    T("%(0to1000)s\n")
        #    + K("c-e"))
        #, "hub": Emacs("cdb/hup")
        #, "hown": Emacs("cdb/hown")
        #, "fup": Emacs("cdb/fup")
        #, "fown": Emacs("cdb/fown")
        #, "tup": Emacs("cdb/tup")
        #, "town": Emacs("cdb/town")
        ## textionary
        , "reload textionary": Emacs("ac-clear-textionary-cache")
        ## buffers
        , "ophyle": Emacs("ido-find-file") # + Emacs("ido-find-file")
        , "ophyle-here": Emacs("ido-find-file")
        , "ophyle <common_file>": Emacs("ido-find-file") + T("%(common_file)s") + K("enter")
        , "ophyle <text>": Emacs("ido-find-file") + T("%(text)s") + K("tab,enter")
        , "rifle": Emacs("recentf-open-files")
        , "(close (buff | buffer | window | file) | clyle)": Emacs("ergoemacs-close-current-buffer") 
        , "pre-buff": Emacs("previous-buffer")
        , "next-buff": Emacs("next-buffer")
        , "bury-buff": Emacs("bury-buffer")
        , "unbury-buff": Emacs("unbury-buffer")
        , "I-buff": Emacs("ibuffer")
        , "e-buff": Emacs("eval-buffer")
        , "(swuff-scratch | swug-scratch)":
            K("c-x") + P("20") + K("b") + T("scratch\n")
        , "(swuff) [<text>]": K("c-x") + P("20") + K("b") + T("%(text)s")
        , "swug <text>": K("c-x") + P("20") + K("b") +
 T("%(text)s") + K("tab,enter")
        , "revert-buffer": Emacs("revert-buffer")
        , "diff-buffer": Emacs("diff-buffer-with-file")
        ## workgroups
        , "create workgroup": Emacs("wg-create-workgroup")
        , "rename workgroup": Emacs("wg-rename-workgroup")
        , "switch workgroup": Emacs("wg-switch-to-workgroup")
        , "clone workgroup": Emacs("wg-clone-workgroup")
        , "revert workgroup": Emacs("wg-revert-workgroup")
        , "update workgroup": Emacs("wg-update-workgroup")
        , "update workgroup": Emacs("wg-update-workgroup")
        , "save workgroup": Emacs("wg-save")
        , "load workgroup": Emacs("wg-load")
        , "workgroup help": Emacs("wg-help")
        ## comments
        , "comment": Emacs("comment-dwim")
        , "comment region": Emacs("comment-region")
        , "kill comment": Emacs("comment-kill")
        , "comment set column": Emacs("comment-set-column")
        ## panes
        , "next-pane": Emacs("ergoemacs-move-cursor-next-pane")
#        , "next-pane": K("a-i")
        , "close-pane": Emacs("delete-window")
        , "close-other-pane": Emacs("delete-other-window")
        , "split-pane": Emacs("split-window-right")
        , "split-pane-horizontally": Emacs("split-window-below")
        ## auto completion
        , "complete": Emacs("auto-complete")
        ## packages
        , "package list": Emacs("package-list-packages")
        , "package initialize": Emacs("package-initialize")
        , "package install [<text>]": Emacs("package-install") + T("%(text)s")
        , "package install file [<text>]": Emacs("package-install-file") + T("%(text)s")
        ## directories

        # macros
        , "start macro": Emacs("start-kbd-macro")

        #, "stop macro": Emacs("end-kbd-macro")
        # Running the text command interferes with the apply macro function. A pause is also required for the keystroke to be recognized correctly.
        , "stop macro": K("c-x") + P("200") + T(")")
        , "run macro": Emacs("call-last-kbd-macro")
        , "apply macro": Emacs("apply-macro-to-region-lines")
        , "name macro": Emacs("name-last-kbd-macro")
        , "save macro": Emacs("insert-kbd-macro")

        }
    defaults = {
        "text":"",
        "0to10000":0,
        "1to10":1,
        "1to10000":1
    }
    extras = [
        chc_base.text,
        chc_base._0to10000,
        chc_base._1to10,
        chc_base._1to10000,
        chc_base.letter_or_digit,
        chc_base.common_file
    ]

'''
        , "(ghin-buffer | ghin-buff)": K("a-langle")
        , "(ex-buffer | ex-buff)": K("a-rangle"

        ## multi-term, shell-command, etc.
        , "(multi-term | termie)": Emacs("dss/multi-term")
        , "term-jump": Emacs("dss/term-cd-dir-path")
        , "shush-term": Emacs("dss/ssh")

        ## operations on Emacs' windows and frames
        , "(window | win) <1to10>": K("a-%(1to10)d")

        , "frot": K("a-1")
        , "frain": K("a-2")
        , "frim": K("a-3")
        , "freer": K("a-4")
        , "froal": K("a-5")
        , "shift <1to10>": (
            K("a-%(1to10)d")
            + Emacs("(progn (dss/screen-buffer 40) (bury-buffer) (delete-window))"))

        , "(winner-back | wack)": Emacs("winner-undo")#K("c-c,left")
        , "(winner-redo | re-wack)": Emacs("winner-redo")#K("c-c,right")
        , "win-right": Emacs("windmove-right")
        , "win-left": Emacs("windmove-left")
        , "win-up": Emacs("windmove-up")
        , "win-down": Emacs("windmove-down")
        # also see the register operations
        , "(other win[dow] | chirp)": K("c-x, o")
        , "(widen | wider) window": K("c-x, rbrace")
        , "(other window quit | other quit | queerp)": K("c-x, o, q")
        , "split [win]": K("c-x, 3")
        , "v-split [win]": K("c-x, 2")
        , "(kill-window | kill-doh)": K("c-x, 0")
        , "clyle-win[dow]": (Emacs("dss/kill-buffer") + K("c-x,0"))
        , "clyle[-win] <1to10>": (K("a-%(1to10)d") + Emacs("dss/kill-buffer") + K("c-x,0"))
        , "(remove window | kill-doh) <1to10>": K("a-%(1to10)d, c-x, 0")
        , "(remove other windows | only-win | O. win)": K("c-x, 1")
        , "oink": K("c-l")              # recenter

        ## operations on sentences
        , "ex-senten": K("a-e")
        , "ghin-senten": K("a-a")
        , "<forward> sentence [<1to10>]": K("a-e:%(1to10)d")
        , "<backward> sentence [<1to10>]": K("a-a:%(1to10)d")
        , "mark-(senten|sentence)": Emacs("k2-mark-whole-sentence")
        , "backward-kill-sentence": Emacs("backward-kill-sentence")
        , "cap-sentence": Emacs("dss/cap-sentence")

        ## operations on paragraphs
        , "(mark-para[graph] | Mara)": K("a-h")
        , "co-para": K("a-h, a-w")
        , "mara-cut": K("a-h, c-w")
        , "mara-chook": K("a-h, backspace")
        , "ghin-para[graph]": K("a-lbrace")
        , "ex-para[graph]": K("a-rbrace")
        , "(<forward> para[graph] | pair down) [<1to10>]": K("a-rbrace:%(1to10)d")
        , "(<backward> para[graph] | pair up) [<1to10>]": K("a-lbrace:%(1to10)d")
        , "(fill-paragraph | fill-para) ": K("a-q")
        , "fill-adapt": Emacs("filladapt-mode")


        ## operations on syntax
        , "(out sexp|sa-oop) [<1to10>]": Emacs("dss/out-one-sexp", narg="1to10")
        , "(forward out sexp | foop)": Emacs("dss/out-one-sexp-forward")
        , "outermost [sexp]": Emacs("dss/out-sexp")
        , "mark-defun": (Emacs("dss/out-sexp")
                         + Emacs("mark-sexp"))
        , "defun-args": Emacs("dss/goto-defun-args")
        , "defun-name": Emacs("dss/goto-defun-name")
        , "defun-docstring": Emacs("dss/goto-defun-docstring")
        , "ex-outermost": (Emacs("dss/out-sexp") + K("ca-f"))
        , "(eval-defun | eol-fund)": Emacs("dss/eval-defun")
        , "mark outermost":(Emacs("dss/out-sexp") + Emacs("mark-sexp"))
        , "mark sexp [<1to10>]": Emacs("mark-sexp", narg="1to10")
        , "(mexp|messed) [<1to10>]": Emacs("mark-sexp", narg="1to10")
        # , "texp": Emacs(
        #     "(progn (mark-sexp) (mark-sexp))")
        , "mank": Emacs("dss/replace-sexp")
        , "moop": (Emacs("dss/out-one-sexp")
                    + Emacs("mark-sexp"))
        , "(jexp|jesp)": Emacs("dss/goto-match-paren")
        , "(copy sexp | kesp)": Emacs("k2-copy-whole-sexp")
        , "kill sexp [<1to10>]": (Emacs("mark-sexp", narg="1to10")+K("c-w"))
        , "<forward> sexp [<1to10>]": K("ca-f:%(1to10)d")
        , "<backward> sexp [<1to10>]": K("ca-b:%(1to10)d")
        , "(ghin-sexp | ghesp)": K("ca-b")
        , "(ex-sexp | fexp | fesp)": K("ca-f")
        , "transpose-sexp": Emacs("transpose-sexps")

        , "(eval-last-sexp|eval-sexp)": K("c-x,c-e")
        , "indent-sexp": Emacs("dss/indent-sexp")
        , "occur defun": Emacs("occur") + T("(defun\n")
        , "copy-defun-name": Emacs("dss/copy-defun-name")

        , "mark block": K("c-c, c-k") + Emacs("k2-toggle-mark") # py-mark-block

        , "(mark <function> | munk)":K("ca-h") # mark-defun
        , "(copy <function> | kunk)":K("ca-h,a-w")
        , "(ghin <function> | gunk)": K("ca-a") # beginning-of-defun
        , "(ex <function> | zunk)": K("ca-e") # end-of-defun

        , "mark class": K("c-u, ca-h")   # py-mark-class
        , "ex-class": K("c-u, ca-e") # py-end-of-class
        , "ghin-class": K("c-u, ca-a") # py-beginning-of-class
        , "next-statement": K("c-c, c-n")
        , "previous-statement": K("c-c, c-p")

        , "ghin-string": (
            Emacs("dss/beginning-of-string")
            + K("right"))
        , "ex-string": (Emacs("dss/end-of-string") + K("left"))
        , "(mark-string | ming | in-ming)": Emacs("dss/mark-string")

        , "baif[-<string>]": Emacs("dss/forward-string")
        , "baif <0to100>": (
            Emacs("dss/local-line-jump")
            + T("%(0to100)s\n")
            + Emacs("dss/forward-string"))
        , "baif <major_system_code>": (
            Emacs("dss/local-line-jump")
            + T("%(major_system_code)s\n")
            + Emacs("dss/forward-string"))
        , "aft-<string>": (Emacs("dss/forward-string")
                          + Emacs("dss/end-of-string")
                          + K("c-b"))
        , "ooft-<string>": (Emacs("dss/backward-string")
                          + Emacs("dss/end-of-string")
                          + K("c-b")
        , "boof[-<string>]": Emacs("dss/backward-string"
        , "maif": (Emacs("dss/forward-string")
        , "chaif": (
            Emacs("dss/forward-string") + Emacs("dss/mark-string") + K("backspace"))
        , "maif <0to100>": (
            Emacs("dss/local-line-jump")
            + T("%(0to100)s\n")
            + Emacs("dss/forward-string")
            + Emacs("dss/mark-string"))

        , "moof": (Emacs("dss/backward-string") + Emacs("dss/mark-string"))
        , "choof": (
            Emacs("dss/backward-string") + Emacs("dss/mark-string") + K("backspace"))
        , "new-<string>": (Emacs("dss/end-of-string")
                             #+ K("c-f")
                             + T(', "'))

        ## completion operations
        , "slam <dict>": (T("%(dict)s") + K("a-slash"))
        , "ace-slam": Emacs("ac-complete")
        , "flam <dict>": (T("%(dict)s") + Emacs("ac-complete-filename"))
        , "flam": Emacs("ac-complete-filename")
        , "(local | low)-flam": Emacs("ac-complete-files-in-current-dir")
        , "(local | low)-flam <dict>": (
            T("%(dict)s") + Emacs("ac-complete-files-in-current-dir"))

        ## operations on whitespace
        , "(fixup space[s] | fix-space)": Emacs("fixup-whitespace")
        , "(clean|fix) whitespace": Emacs("dss/whitespace-cleanup")
        , "(strip-space|speece)": Emacs("dss/del-last-space")
        , "spice": Emacs("dss/del-last-space-2")
        , "(less-space|spooce)": Emacs("dss/less-space")
        , "sleece": K("c-e,c-k,f4,space")


'''

class DiredRule(MappingRule):
    mapping = {
        "die [<common_folder>]": Emacs("dired") + T("%(common_folder)s") + K("enter")
        , "die to": Emacs("dired-goto-file")           
        , "die tox <text>": Emacs("dired-goto-file") + T("%(text)s\n")
        , "die find": Emacs("dired-isearch-filenames")
        , "die up": Emacs("dired-up-directory-reuse-dir-buffer")
        , "die image[s]": Emacs("image-dired")
        , "die this image[s]": Emacs("image-dired-display-thumbs")
        , "die flag": Emacs("dired-flag-file-deletion")
        , "die unflag": Emacs("dired-unmark")
        , "die unflag all": Emacs("dired-unmark-all-marks")
        , "die unflag back": Emacs("dired-unmark-backward")        
        , "die flag delete": Emacs("dired-do-flagged-delete")
        , "die flag backup": Emacs("dired-flag-backup-files")
        , "die flag auto save": Emacs("dired-flag-auto-save-files")
        , "die flag regex": Emacs("dired-flag-files-regexp")
        , "die next flag": Emacs("dired-next-marked-file")
        , "die pre flag": Emacs("dired-prev-marked-file")
        , "die undo": Emacs("dired-undo")
        , "(die cop | die copy)": Emacs("dired-do-copy")
        , "(die dell | die delete)": Emacs("dired-do-delete")
        , "(die re | die rename)": Emacs("dired-do-renamed")
        , "(die hard | die hard link )": Emacs("dired-do-hardlink")
        , "(die sim | die  sym link)": Emacs("dired-do-symlink")
        , "die mod": Emacs("dired-do-chmod")
        , "(die own | die owner)": Emacs("dired-do-chown")
        , "die group": Emacs("dired-do-chgrp")
        , "die touch": Emacs("dired-do-touch")
        , "die print": Emacs("dired-do-print")
        , "die compress": Emacs("dired-do-compress")
        , "die encrypt": Emacs("dired-do-encrypt")
        , "die decrypt": Emacs("dired-do-decrypt")
        , "die sign": Emacs("dired-do-sign")
        , "die verify": Emacs("dired-do-verify")
        , "die load": Emacs("dired-do-load")
        , "die compile": Emacs("dired-do-compile")
        , "die search": Emacs("dired-do-search")
        , "die query": Emacs("dired-do-query-replace-regexp")
        , "die shell": Emacs("dired-do-shell-command")
        , "die refresh": Emacs("revert-buffer")
        , "die order": Emacs("dired-sort-toggle-or-edit")
        , "(die die | die make directory)": Emacs("dired-create-directory")
        , "die (op | open)": Emacs("dired-find-file")
        , "die (op | open) other": Emacs("dired-find-file-other-window")
        , "die (win | windows)": Emacs("dired-w32-browser")
        , "die (win | windows) same": Emacs("dired-w32-browser-reuse-dir-buffer")
        , "die (ex | explorer)": Emacs("dired-w32explore")
        , "(direct | directory) <common_folder>": T("%(common_folder)s\n")
    }
    defaults = {
        "text":"",
        "folder":""
    }
    extras = [
        chc_base.text
        , chc_base.common_folder
    ]

class EshellRule(MappingRule):
    mapping = {
        "kill eshell": T("(let ((inhibit-read-only t)) (kill-this-buffer))\n")
        , "chai (op | open)": T("find-file ")
        , "chai (op | open) <text>": T("find-file %(text)s") + K("tab,enter")
        , "chai (win | windows)": T("op ")
        , "chai (win | windows) <text>": T("op %(text)s") + K("tab,enter")
        , "chai (ex | explorer)": T("ex ")
        , "chai (ex | explorer) <text>": T("ex %(text)s") + K("tab,enter")
        , "chai (ex | explorer) (here | this)": T("ex .\n")
    }
    defaults = {
        "text":""
    }
    extras = [
        chc_base.text
        , chc_base._1to10
    ]

class ErcRule(MappingRule):
    mapping = {
        "(ERC | IRC)": Emacs("cdb-erc")
    }
    defaults = {
        "text":""
    }
    extras = [
        chc_base.text
        , chc_base._1to10
    ]

#---------------------------------------------------------------------------
# HTML Rule
#---------------------------------------------------------------------------

class EmacsHtmlRule(MappingRule):
    mapping = {
        # general
        "tag nav": Emacs("web-mode-navigate") # K("c-c,c-n")
        , "fold": Emacs("web-mode-fold-or-unfold") #K("c-c,c-f")
        , "snip": Emacs("web-mode-snippet-insert") # K("c-c,c-s")
        , "comment": Emacs("web-mode-comment-or-uncomment") # K("c-c,c-semicolon")
        , "select": Emacs("web-mode-mark-and-expand") # K("c-c,c-m")
        , "whitespace": Emacs("web-mode-whitespaces-show") # K("c-c,c-w")
        , "indent": Emacs("web-mode-buffer-indent") # K("c-c,c-i")
#        , "highlight": Emacs("web-mode-buffer-highlight")
        # element
        , "elem start": Emacs("web-mode-element-beginning")
        , "elem clone": Emacs("web-mode-element-clone")
        , "elem down": Emacs("web-mode-element-child")
        , "elem end": Emacs("web-mode-element-end")
        , "elem fold": Emacs("web-mode-element-children-fold-or-unfold")
        , "elem content": Emacs("web-mode-element-content-select")
        , "elem delete": Emacs("web-mode-element-kill")
        , "elem blanks": Emacs("web-mode-element-mute-blanks")
        , "elem next": Emacs("web-mode-element-next")
        , "elem pre": Emacs("web-mode-element-previous")
        , "elem rename": Emacs("web-mode-element-rename")
        , "elem select": Emacs("web-mode-element-select")
        , "elem (trans | transpose)": Emacs("web-mode-element-transpose")
        , "elem up": Emacs("web-mode-element-parent")
        , "elem vanish": Emacs("web-mode-element-vanish")
        , "elem web": Emacs("web-mode-element-wrap")
        # attribute
        , "attrib start": Emacs("web-mode-attribute-beginning")
        , "attrib end": Emacs("web-mode-attribute-end")
        , "attrib next": Emacs("web-mode-attribute-next")
        # tag
#        , "at sort": Emacs("web-mode-tag-attributes-sort")
        , "at start": Emacs("web-mode-tag-beginning")
        , "at end": Emacs("web-mode-tag-end")
        , "at match": Emacs("web-mode-tag-match")
        , "at next": Emacs("web-mode-tag-next")
        , "at pre": Emacs("web-mode-tag-previous")
        , "at select": Emacs("web-mode-tag-select")
        # block
        , "bee close": Emacs("web-mode-block-close")
        , "bee start": Emacs("web-mode-block-beginning")
        , "bee end": Emacs("web-mode-block-end")
        , "bee delete": Emacs("web-mode-block-kill")
        , "bee next": Emacs("web-mode-block-next")
        , "bee pre": Emacs("web-mode-block-previous")
        , "bee select": Emacs("web-mode-block-select")
        # dom
        , "dom replace apos": Emacs("web-mode-dom-apostrophes-replace")
        , "dom normalize": Emacs("web-mode-dom-normalize")
        , "dom check": Emacs("web-mode-dom-errors-show")
        , "dom replace entities": Emacs("web-mode-dom-entities-replace")
        , "dom replace quotes": Emacs("web-mode-dom-quotes-replace")
        , "dom traverse": Emacs("web-mode-dom-traverse")
        , "dom ex path": Emacs("web-mode-dom-xpath")
    }
    defaults = {
    }
    extras = [
    ]
