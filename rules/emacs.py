import choices.base as chc_base

from dragonfly import (
    MappingRule
)

from util import (
    K,
    T,
    P,
    emacs
)

#---------------------------------------------------------------------------
# Core Rule
#---------------------------------------------------------------------------

class EmacsBaseRule(MappingRule):
    mapping = {
        "(quit | escape) [<1to100>]": K("c-g:%(1to100)d")
        , "quit quit": K("c-g:2")
        , "quit quit quit": K("c-g:3")
        , "(cop | copy)": emacs("clipboard-kill-ring-save")
        , "cut": emacs("clipboard-kill-region")
        , "paste": emacs("clipboard-yank")
        , "foo [<1to100>]": emacs("forward-word")
        , "foo foo": emacs("forward-word,")
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
        , "eslap": emacs("move-end-of-line") + K("enter")
        , "dotslap": emacs("move-end-of-line") + K("dot, enter")
        , "camslap": emacs("move-end-of-line") + K("comma, enter")
        , "semslap": emacs("move-end-of-line") + T(";") + K("enter")
        , "coalslap": emacs("move-end-of-line") + K("colon, enter")
        , "altslap": K("a,enter")
        , "(downslap | deeslap)": K("down,enter")
        , "(tap | tab) [<1to100>]": K("tab:%(1to100)d")
        , "tab tab": K("tab:2")
        , "tab tab tab": K("tab:3")
        , "home": emacs("move-beginning-of-line")
        , "end": emacs("move-end-of-line")
        , "u-end": K("up") + emacs("move-end-of-line")
        , "de-end": K("down") + emacs("move-end-of-line")
        , "sellome": K("s-home")
        , "deelome": K("s-home, backspace")
        , "sellend": K("s-end")
        , "deelend": K("s-end, backspace")
        , "cleeline": K("home") + K("s-down:%(0to100)d") + K("s-end") + K("backspace:2,enter")
        , "selline [<0to100>]": K("home") + K("s-down:%(0to100)d") + K("s-end")
        , "deeline [<0to100>]": K("home") + K("s-down:%(0to100)d") + K("s-end") + K("backspace:2")
        , "coline [<0to100>]": K("home") + K("s-down:%(0to100)d") + K("s-end") + K("c-c")
        , "dupline  [<0to100>] [<1to10>]": K("home") + K("s-down:%(0to100)d") + K("s-end") + P("20") + K("c-c") + P("20") + K("enter") + K("c-v:%(1to10)d") # c-c needs to be isolated with medium pauses!!!
        , "go to home": emacs("beginning-of-buffer")
        , "go to end": emacs("end-of-buffer")
        , "Apple": emacs("end-of-buffer")
    }
    defaults = {
        "0to100":0,
        "1to10":1,
        "1to100":1,
        "1to10000":1
    }
    extras = [
        chc_base._0to100,
        chc_base._1to10,
        chc_base._1to100,
        chc_base._1to10000
    ]

#---------------------------------------------------------------------------
# Core Rule
#---------------------------------------------------------------------------

class EmacsCoreRule(MappingRule):
    mapping = {
        "command": K("a-u")
        , "elast": emacs("eval-print-last-sexp")
        
        , "close emacs": emacs("save-buffers-kill-terminal")
        , "(eshell | shell) [<1to10>]": K("c-%(1to10)s") + emacs("eshell")
        ## bindings
        , "describe function": emacs("describe-function")
        , "describe key": emacs("describe-key")
        ## chars
        , "unicode": emacs("insert-char")
        , "transpose-chars": emacs("transpose-chars")
        ## words
        , "transpose-words":  emacs("transpose-words")
        , "replace word [with] <text>": emacs("kill-word") + T("%(text)s")
        , "replace last word [with] <text>": emacs("backward-word") + emacs("kill-word") + T("%(text)s")
        , "(downcase word | down-word)": emacs("downcase-word")
        , "downcase last": emacs("(downcase-word -1)")
        , "(upcase word | up-word)": emacs("upcase-word")
        , "upcase last": emacs("(upcase-word -1)")
        , "(capitalize | cap) word": emacs("capitalize-word")
        , "cap last [word]": emacs("(capitalize-word -1)")
        , "sub-word-mode": emacs("subword-mode")
        ## lines
        , "sort-lines": emacs("sort-lines")
        , "(transpose-lines | trans-lines)": emacs("transpose-lines")
        , "sort-columns": emacs("sort-columns")
        , "flush-lines": emacs("flush-lines")
        , "keep-lines": emacs("keep-lines")
        , "align-regexp": emacs("align-regexp")
        , "selline <0to10000> to <1to10000>": emacs("goto-line") + T("%(0to10000)d\n") + K("home") + emacs("set-mark-command") + emacs("goto-line") + T("%(1to10000)d\n") + K("end")
#        , "open-line [<1to10>]": emacs("dss/-open-line-indent", narg='1to10')
#        , "(o-line | jab)": emacs("dss/smart-open-line")
        , "count lines": emacs("count-lines-region")
        , "count lines page": emacs("count-lines-page")
        ## registers
        , "ropy <letter_or_digit>": emacs("copy-to-register") + T("%(letter_or_digit)s")
        , "repend <letter_or_digit>": emacs("prepend-to-register") + T("%(letter_or_digit)s")
        , "rapend <letter_or_digit>": emacs("append-to-register") + T("%(letter_or_digit)s")
        , "raste <letter_or_digit>": emacs("insert-register") + T("%(letter_or_digit)s")
        , "roint <letter_or_digit>": emacs("point-to-register") + T("%(letter_or_digit)s")
        , "reroint <letter_or_digit>": emacs("register-to-point") + T("%(letter_or_digit)s")
        , "rump <letter_or_digit>": emacs("jump-to-register") + T("%(letter_or_digit)s")
        , "rump": emacs("jump-to-register")
        , "rist": emacs("list-registers")
        , "rindow[s] <letter_or_digit>": emacs("window-configuration-to-register") + T("%(letter_or_digit)s")
        , "rame[s] <letter_or_digit>": emacs("frame-configuration-to-register") + K("%(letter_or_digit)s")
        , "ruffer": emacs("undo-tree-save-state-to-register")
        , "reruffer": emacs("undo-tree-restore-state-to-register")
        ## mark
        , "[set] mark": emacs("set-mark-command")
        , "sell up": emacs("set-mark-command") + K("up")
        , "sell down": emacs("set-mark-command") + K("down")
        , "point mark": emacs("set-mark-command") + emacs("set-mark-command")
        , "visible-marks": emacs("visible-mark-mode")
        , "swap mark": emacs("exchange-point-and-mark")
        , "jump mark": emacs("pop-to-mark-command")
        , "glo[bal]-jark": emacs("pop-global-mark")
        #, "(toggle mark | mark off | tark)": emacs("k2-toggle-mark")
        #, sharks
        , "highline mode": emacs("hl-line-mode")
        ## operations on special markers
        #, "skack": emacs("(dss/skeleton-next-position t)")
        #, "skext": emacs("dss/skeleton-next-position")
        ## region
        , "(capitalize|cap) [(region | it)]": emacs("capitalize-region")
        , "downcase [(region | it)]": emacs("downcase-region")
        , "upcase [(region | it)]": emacs("upcase-region")
        #, "quote-(region | it)": emacs("dss/quote-region")
        #, "stud-(region | it)": emacs("dss/words-studley-region")
        #, "jive-stud-(region | it)": emacs("dss/words-studley-to-sep-region")
        #, "single-quote-region": emacs("dss/single-quote-region")
        #, "(eval | evaluate) region": emacs("eval-region")
        , "flash-region": emacs("dss/flash-region")
        , "indent-region": emacs("indent-region")
        , "narrow-to-region": emacs("narrow-to-region")
        , "widen-to-buffer": emacs("widen-to-buffer")
        #  the following two commands assume that the region has the
        #  point at the top and the mark at the bottom
        #, "shrink-region [<1to10>]": K(
        #    "right:%(1to10)d,c-x,c-x,left:%(1to10)d,c-x,c-x")
        #, "shrink-region by <1to10> line[s]": K(
        #    "down:%(1to10)d,c-x,c-x,up:%(1to10)d,c-x,c-x")
        ## kill ring
        , "kill-ring": emacs("browse-kill-ring")
        # goto
        , "goost": emacs("goto-last-change")
        , "em-goost": emacs("goto-last-change-with-auto-marks")
        , "line <1to10000>": emacs("goto-line") + T("%(1to10000)d\n") + emacs("back-to-indentation")        
        ## movement
        , "snap": emacs("back-to-indentation")
        , "de-snap": K("down") + emacs("back-to-indentation")
        , "u-snap": K("up") + emacs("back-to-indentation")
        #, "snap <0to1000>": (
        #    emacs("dss/local-line-jump")
        #    + T("%(0to1000)s\n"))
        #, "(eol | yall | y'all) <0to1000>": (
        #    emacs("dss/local-line-jump") +
        #    T("%(0to1000)s\n")
        #    + K("c-e"))
        #, "hub": emacs("cdb/hup")
        #, "hown": emacs("cdb/hown")
        #, "fup": emacs("cdb/fup")
        #, "fown": emacs("cdb/fown")
        #, "tup": emacs("cdb/tup")
        #, "town": emacs("cdb/town")
        ## textionary
        , "reload textionary": emacs("ac-clear-textionary-cache")
        ## buffers
        , "ophyle": emacs("ido-find-file") # + emacs("ido-find-file")
        , "ophyle-here": emacs("ido-find-file")
        , "ophyle <common_file>": emacs("ido-find-file") + T("%(common_file)s") + K("enter")
        , "ophyle <text>": emacs("ido-find-file") + T("%(text)s") + K("tab,enter")
        , "rifle": emacs("recentf-open-files")
        , "(close (buff | buffer | window | file) | clyle)": emacs("ergoemacs-close-current-buffer") 
        , "pre-buff": emacs("previous-buffer")
        , "next-buff": emacs("next-buffer")
        , "bury-buff": emacs("bury-buffer")
        , "unbury-buff": emacs("unbury-buffer")
        , "I-buff": emacs("ibuffer")
        , "e-buff": emacs("eval-buffer")
        , "(swuff-scratch | swug-scratch)":
            K("c-x") + P("20") + K("b") + T("scratch\n")
        , "(swuff) [<text>]": K("c-x") + P("20") + K("b") + T("%(text)s")
        , "swug <text>": K("c-x") + P("20") + K("b") +
 T("%(text)s") + K("tab,enter")
        , "revert-buffer": emacs("revert-buffer")
        , "diff-buffer": emacs("diff-buffer-with-file")
        ## workgroups
        , "create workgroup": emacs("wg-create-workgroup")
        , "rename workgroup": emacs("wg-rename-workgroup")
        , "switch workgroup": emacs("wg-switch-to-workgroup")
        , "clone workgroup": emacs("wg-clone-workgroup")
        , "revert workgroup": emacs("wg-revert-workgroup")
        , "update workgroup": emacs("wg-update-workgroup")
        , "update workgroup": emacs("wg-update-workgroup")
        , "save workgroup": emacs("wg-save")
        , "load workgroup": emacs("wg-load")
        , "workgroup help": emacs("wg-help")
        ## comments
        , "comment": emacs("comment-dwim")
        , "comment region": emacs("comment-region")
        , "kill comment": emacs("comment-kill")
        , "comment set column": emacs("comment-set-column")
        ## panes
        , "next-pane": emacs("ergoemacs-move-cursor-next-pane")
#        , "next-pane": K("a-i")
        , "close-pane": emacs("delete-window")
        , "close-other-pane": emacs("delete-other-window")
        , "split-pane": emacs("split-window-right")
        , "split-pane-horizontally": emacs("split-window-below")
        ## auto completion
        , "complete": emacs("auto-complete")
        ## packages
        , "package list": emacs("package-list-packages")
        , "package initialize": emacs("package-initialize")
        , "package install [<text>]": emacs("package-install") + T("%(text)s")
        , "package install file [<text>]": emacs("package-install-file") + T("%(text)s")
        ## directories

        # macros
        , "start macro": emacs("start-kbd-macro")

        #, "stop macro": emacs("end-kbd-macro")
        # Running the text command interferes with the apply macro function. A pause is also required for the keystroke to be recognized correctly.
        , "stop macro": K("c-x") + P("200") + T(")")
        , "run macro": emacs("call-last-kbd-macro")
        , "apply macro": emacs("apply-macro-to-region-lines")
        , "name macro": emacs("name-last-kbd-macro")
        , "save macro": emacs("insert-kbd-macro")

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
        , "(multi-term | termie)": emacs("dss/multi-term")
        , "term-jump": emacs("dss/term-cd-dir-path")
        , "shush-term": emacs("dss/ssh")

        ## operations on Emacs' windows and frames
        , "(window | win) <1to10>": K("a-%(1to10)d")

        , "frot": K("a-1")
        , "frain": K("a-2")
        , "frim": K("a-3")
        , "freer": K("a-4")
        , "froal": K("a-5")
        , "shift <1to10>": (
            K("a-%(1to10)d")
            + emacs("(progn (dss/screen-buffer 40) (bury-buffer) (delete-window))"))

        , "(winner-back | wack)": emacs("winner-undo")#K("c-c,left")
        , "(winner-redo | re-wack)": emacs("winner-redo")#K("c-c,right")
        , "win-right": emacs("windmove-right")
        , "win-left": emacs("windmove-left")
        , "win-up": emacs("windmove-up")
        , "win-down": emacs("windmove-down")
        # also see the register operations
        , "(other win[dow] | chirp)": K("c-x, o")
        , "(widen | wider) window": K("c-x, rbrace")
        , "(other window quit | other quit | queerp)": K("c-x, o, q")
        , "split [win]": K("c-x, 3")
        , "v-split [win]": K("c-x, 2")
        , "(kill-window | kill-doh)": K("c-x, 0")
        , "clyle-win[dow]": (emacs("dss/kill-buffer") + K("c-x,0"))
        , "clyle[-win] <1to10>": (K("a-%(1to10)d") + emacs("dss/kill-buffer") + K("c-x,0"))
        , "(remove window | kill-doh) <1to10>": K("a-%(1to10)d, c-x, 0")
        , "(remove other windows | only-win | O. win)": K("c-x, 1")
        , "oink": K("c-l")              # recenter

        ## operations on sentences
        , "ex-senten": K("a-e")
        , "ghin-senten": K("a-a")
        , "<forward> sentence [<1to10>]": K("a-e:%(1to10)d")
        , "<backward> sentence [<1to10>]": K("a-a:%(1to10)d")
        , "mark-(senten|sentence)": emacs("k2-mark-whole-sentence")
        , "backward-kill-sentence": emacs("backward-kill-sentence")
        , "cap-sentence": emacs("dss/cap-sentence")

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
        , "fill-adapt": emacs("filladapt-mode")


        ## operations on syntax
        , "(out sexp|sa-oop) [<1to10>]": emacs("dss/out-one-sexp", narg="1to10")
        , "(forward out sexp | foop)": emacs("dss/out-one-sexp-forward")
        , "outermost [sexp]": emacs("dss/out-sexp")
        , "mark-defun": (emacs("dss/out-sexp")
                         + emacs("mark-sexp"))
        , "defun-args": emacs("dss/goto-defun-args")
        , "defun-name": emacs("dss/goto-defun-name")
        , "defun-docstring": emacs("dss/goto-defun-docstring")
        , "ex-outermost": (emacs("dss/out-sexp") + K("ca-f"))
        , "(eval-defun | eol-fund)": emacs("dss/eval-defun")
        , "mark outermost":(emacs("dss/out-sexp") + emacs("mark-sexp"))
        , "mark sexp [<1to10>]": emacs("mark-sexp", narg="1to10")
        , "(mexp|messed) [<1to10>]": emacs("mark-sexp", narg="1to10")
        # , "texp": emacs(
        #     "(progn (mark-sexp) (mark-sexp))")
        , "mank": emacs("dss/replace-sexp")
        , "moop": (emacs("dss/out-one-sexp")
                    + emacs("mark-sexp"))
        , "(jexp|jesp)": emacs("dss/goto-match-paren")
        , "(copy sexp | kesp)": emacs("k2-copy-whole-sexp")
        , "kill sexp [<1to10>]": (emacs("mark-sexp", narg="1to10")+K("c-w"))
        , "<forward> sexp [<1to10>]": K("ca-f:%(1to10)d")
        , "<backward> sexp [<1to10>]": K("ca-b:%(1to10)d")
        , "(ghin-sexp | ghesp)": K("ca-b")
        , "(ex-sexp | fexp | fesp)": K("ca-f")
        , "transpose-sexp": emacs("transpose-sexps")

        , "(eval-last-sexp|eval-sexp)": K("c-x,c-e")
        , "indent-sexp": emacs("dss/indent-sexp")
        , "occur defun": emacs("occur") + T("(defun\n")
        , "copy-defun-name": emacs("dss/copy-defun-name")

        , "mark block": K("c-c, c-k") + emacs("k2-toggle-mark") # py-mark-block

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
            emacs("dss/beginning-of-string")
            + K("right"))
        , "ex-string": (emacs("dss/end-of-string") + K("left"))
        , "(mark-string | ming | in-ming)": emacs("dss/mark-string")

        , "baif[-<string>]": emacs("dss/forward-string")
        , "baif <0to100>": (
            emacs("dss/local-line-jump")
            + T("%(0to100)s\n")
            + emacs("dss/forward-string"))
        , "baif <major_system_code>": (
            emacs("dss/local-line-jump")
            + T("%(major_system_code)s\n")
            + emacs("dss/forward-string"))
        , "aft-<string>": (emacs("dss/forward-string")
                          + emacs("dss/end-of-string")
                          + K("c-b"))
        , "ooft-<string>": (emacs("dss/backward-string")
                          + emacs("dss/end-of-string")
                          + K("c-b")
        , "boof[-<string>]": emacs("dss/backward-string"
        , "maif": (emacs("dss/forward-string")
        , "chaif": (
            emacs("dss/forward-string") + emacs("dss/mark-string") + K("backspace"))
        , "maif <0to100>": (
            emacs("dss/local-line-jump")
            + T("%(0to100)s\n")
            + emacs("dss/forward-string")
            + emacs("dss/mark-string"))

        , "moof": (emacs("dss/backward-string") + emacs("dss/mark-string"))
        , "choof": (
            emacs("dss/backward-string") + emacs("dss/mark-string") + K("backspace"))
        , "new-<string>": (emacs("dss/end-of-string")
                             #+ K("c-f")
                             + T(', "'))

        ## completion operations
        , "slam <dict>": (T("%(dict)s") + K("a-slash"))
        , "ace-slam": emacs("ac-complete")
        , "flam <dict>": (T("%(dict)s") + emacs("ac-complete-filename"))
        , "flam": emacs("ac-complete-filename")
        , "(local | low)-flam": emacs("ac-complete-files-in-current-dir")
        , "(local | low)-flam <dict>": (
            T("%(dict)s") + emacs("ac-complete-files-in-current-dir"))

        ## operations on whitespace
        , "(fixup space[s] | fix-space)": emacs("fixup-whitespace")
        , "(clean|fix) whitespace": emacs("dss/whitespace-cleanup")
        , "(strip-space|speece)": emacs("dss/del-last-space")
        , "spice": emacs("dss/del-last-space-2")
        , "(less-space|spooce)": emacs("dss/less-space")
        , "sleece": K("c-e,c-k,f4,space")


'''

class DiredRule(MappingRule):
    mapping = {
        "die [<common_folder>]": emacs("dired") + T("%(common_folder)s") + K("enter")
        , "die to": emacs("dired-goto-file")           
        , "die tox <text>": emacs("dired-goto-file") + T("%(text)s\n")
        , "die find": emacs("dired-isearch-filenames")
        , "die up": emacs("dired-up-directory-reuse-dir-buffer")
        , "die image[s]": emacs("image-dired")
        , "die this image[s]": emacs("image-dired-display-thumbs")
        , "die flag": emacs("dired-flag-file-deletion")
        , "die unflag": emacs("dired-unmark")
        , "die unflag all": emacs("dired-unmark-all-marks")
        , "die unflag back": emacs("dired-unmark-backward")        
        , "die flag delete": emacs("dired-do-flagged-delete")
        , "die flag backup": emacs("dired-flag-backup-files")
        , "die flag auto save": emacs("dired-flag-auto-save-files")
        , "die flag regex": emacs("dired-flag-files-regexp")
        , "die next flag": emacs("dired-next-marked-file")
        , "die pre flag": emacs("dired-prev-marked-file")
        , "die undo": emacs("dired-undo")
        , "(die cop | die copy)": emacs("dired-do-copy")
        , "(die dell | die delete)": emacs("dired-do-delete")
        , "(die re | die rename)": emacs("dired-do-renamed")
        , "(die hard | die hard link )": emacs("dired-do-hardlink")
        , "(die sim | die  sym link)": emacs("dired-do-symlink")
        , "die mod": emacs("dired-do-chmod")
        , "(die own | die owner)": emacs("dired-do-chown")
        , "die group": emacs("dired-do-chgrp")
        , "die touch": emacs("dired-do-touch")
        , "die print": emacs("dired-do-print")
        , "die compress": emacs("dired-do-compress")
        , "die encrypt": emacs("dired-do-encrypt")
        , "die decrypt": emacs("dired-do-decrypt")
        , "die sign": emacs("dired-do-sign")
        , "die verify": emacs("dired-do-verify")
        , "die load": emacs("dired-do-load")
        , "die compile": emacs("dired-do-compile")
        , "die search": emacs("dired-do-search")
        , "die query": emacs("dired-do-query-replace-regexp")
        , "die shell": emacs("dired-do-shell-command")
        , "die refresh": emacs("revert-buffer")
        , "die order": emacs("dired-sort-toggle-or-edit")
        , "(die die | die make directory)": emacs("dired-create-directory")
        , "die (op | open)": emacs("dired-find-file")
        , "die (op | open) other": emacs("dired-find-file-other-window")
        , "die (win | windows)": emacs("dired-w32-browser")
        , "die (win | windows) same": emacs("dired-w32-browser-reuse-dir-buffer")
        , "die (ex | explorer)": emacs("dired-w32explore")
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
        , "choi (op | open) <text>": T("find-file %(text)s") + K("tab,enter")
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
        "(ERC | IRC)": emacs("erc")
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

class HtmlRule(MappingRule):
    mapping = {
        # general
        "tag nav": emacs("web-mode-navigate") # K("c-c,c-n")
        , "fold": emacs("web-mode-fold-or-unfold") #K("c-c,c-f")
        , "snip": emacs("web-mode-snippet-insert") # K("c-c,c-s")
        , "comment": emacs("web-mode-comment-or-uncomment") # K("c-c,c-semicolon")
        , "select": emacs("web-mode-mark-and-expand") # K("c-c,c-m")
        , "whitespace": emacs("web-mode-whitespaces-show") # K("c-c,c-w")
        , "indent": emacs("web-mode-buffer-indent") # K("c-c,c-i")
#        , "highlight": emacs("web-mode-buffer-highlight")
        # element
        , "elem start": emacs("web-mode-element-beginning")
        , "elem clone": emacs("web-mode-element-clone")
        , "elem down": emacs("web-mode-element-child")
        , "elem end": emacs("web-mode-element-end")
        , "elem fold": emacs("web-mode-element-children-fold-or-unfold")
        , "elem content": emacs("web-mode-element-content-select")
        , "elem delete": emacs("web-mode-element-kill")
        , "elem blanks": emacs("web-mode-element-mute-blanks")
        , "elem next": emacs("web-mode-element-next")
        , "elem pre": emacs("web-mode-element-previous")
        , "elem rename": emacs("web-mode-element-rename")
        , "elem select": emacs("web-mode-element-select")
        , "elem (trans | transpose)": emacs("web-mode-element-transpose")
        , "elem up": emacs("web-mode-element-parent")
        , "elem vanish": emacs("web-mode-element-vanish")
        , "elem web": emacs("web-mode-element-wrap")
        # attribute
        , "attrib start": emacs("web-mode-attribute-beginning")
        , "attrib end": emacs("web-mode-attribute-end")
        , "attrib next": emacs("web-mode-attribute-next")
        # tag
#        , "at sort": emacs("web-mode-tag-attributes-sort")
        , "at start": emacs("web-mode-tag-beginning")
        , "at end": emacs("web-mode-tag-end")
        , "at match": emacs("web-mode-tag-match")
        , "at next": emacs("web-mode-tag-next")
        , "at pre": emacs("web-mode-tag-previous")
        , "at select": emacs("web-mode-tag-select")
        # block
        , "bee close": emacs("web-mode-block-close")
        , "bee start": emacs("web-mode-block-beginning")
        , "bee end": emacs("web-mode-block-end")
        , "bee delete": emacs("web-mode-block-kill")
        , "bee next": emacs("web-mode-block-next")
        , "bee pre": emacs("web-mode-block-previous")
        , "bee select": emacs("web-mode-block-select")
        # dom
        , "dom replace apos": emacs("web-mode-dom-apostrophes-replace")
        , "dom normalize": emacs("web-mode-dom-normalize")
        , "dom check": emacs("web-mode-dom-errors-show")
        , "dom replace entities": emacs("web-mode-dom-entities-replace")
        , "dom replace quotes": emacs("web-mode-dom-quotes-replace")
        , "dom traverse": emacs("web-mode-dom-traverse")
        , "dom ex path": emacs("web-mode-dom-xpath")
    }
    defaults = {
    }
    extras = [
    ]
