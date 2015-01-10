from dragonfly import MappingRule

from actions.action_shortcut import (
    K,
    T,
    P,
    M
)

import choices.base as chc_base

#---------------------------------------------------------------------------
# Core Rule
#---------------------------------------------------------------------------

class ShellCoreRule(MappingRule):
    mapping = {
        "exit": T("exit\n")
        , "alias": T("alias ")
        , "cat": T("cat ")
        , "shell copy": T("cp ")
        , "chai": T("cd ") 
        , "chai <text>": T("cd %(text)s")  + K("tab,enter")
        , "chai chain <text>": T("cd %(text)s")  + K("tab:3")
        , "chain <text>": T("%(text)s") + K("tab:3")
        , "chai up": T("cd ..\n")
        , "chaif <common_folder>": T("cd %(common_folder)s\n") 
        , "differences": T("diff ")
        , "disk usage": T("du -ch\n")
        , "disk usage all": T("du -ach\n")
        , "echo": T("echo ")
        , "echo path": T("echo $PATH\n")
        , "environment": T("env\n")
        , "glimpse": T("glimpse ")
        , "<grep>": T("%(grep)s -rin -B2 -A2 '' .") + K("left:3")
        , "<grep> <text>": T("%(grep)s -rin -B2 -A2 '%(text)s' .\n")
        , "info documentation": T("info ")
        , "jobs": T("jobs -l\n")
        , "jobs running": T("jobs -lr\n")
        , "jobs stopped": T("jobs -ls\n")
        , "kill process": T("kill ")
        , "kill process now": T("kill -9 ")
        , "link soft": T("ln -s ")
        , "link hard": T("ln ")
        , "list": T("ls -la\n")
        , "list <text>": T("ls -la %(text)s") + K("tab,enter")
        , "list chain <text>": T("ls -la %(text)s") + K("tab:3")
        , "list up": T("ls -la ..\n")
        , "list up up": T("ls -la ../..\n")
        , "locate": T("locate ")
        , "locate update": T("updatedb\n")
        , "man page": T("man ")
        , "chai chai": T("mkdir ")
        , "chai chai <text>": T("mkdir %(text)s\n")
        , "chai chai parent": T("mkdir -p ")
        , "chai chai parent <text>": T("mkdir -p %(text)s\n")
        , "move": T("mv ")
        , "move <text> to [<text2>]": T("mv %(text)s") + K("tab") + T(" %(text2)s") + K("tab")
        , "push (directory | chai)": T("pushd .\n")
        , "push other (directory | chai)": T("pushd ")
        , "pop (directory | chai)": T("popd\n")
        , "(directory | chai) stack": T("dirs\n")
        , "print (working directory | chai)": T("pwd\n")
        , "remove": T("rm ")
        , "remove (directory | chai)": T("rmdir ")
        , "remove (directory | chai) recursively": T("rmdir -r")
        , "run": T("./")
        , "run <text>": T("./%(text)s") + K("tab,enter")
        , "(sudo | super [user] do)": T("sudo ")
        , "switch user": T("su ")
        , "switch user <os_user>": T("su %(os_user)s\n")
        , "time": T("time ")
        , "user mask": T("umask ")
        , "who am I": T("whoami\n")
        , "help flag": T(" --help")
        , "help flag short": T(" -h")
        , "verbose flag": T(" --verbose")
        , "verbose flag short": T(" -v")
        , "run updates": T("runupdates \n")
        , "force updates": T("runupdates -f\n")
        , "check updates": T("checkupdates\n")
        , "restart": T("sudo shutdown -r now\n")
        , "reboot": T("sudo reboot\n")
        , "shutdown": T("sudo shutdown now\n")
        , "shaste": M("(0.5, 0.5), right")
        # tools
        , "apt[itude] search": T("sudo aptitude search ")
        , "apt[itude] install": T("sudo aptitude install ")
        , "apt[itude] show": T("sudo aptitude show ")
        , "apt[itude] update": T("sudo aptitude update\n")
        , "apt[itude] upgrade": T("sudo aptitude update && aptitude upgrade\n")
        , "gem[s] chek": T("gem outdated\n")
        , "gem[s] update": T("gem update\n")
        , "MD 5 check": T("md5sum -c ")
        , "root kit Hunter check": T("rkhunter --check\n")
        , "root kit Hunter update": T("rkhunter --propupd\n")
        , "check root kit": T("chkrootkit\n") 
        , "web get": T("wget ")
        , "vim": T("vi ")
        , "vim <text>": T("vi %(text)s") + K("tab,enter")        
        , "vimf <common_file>": T("vi %(common_file)s\n")
        , "vimslap": T("vi\n")
        , "suvim": T("sudo vi ")
        , "suvim <text>": T("sudo vi %(text)s") + K("tab,enter")        
        , "suvimf <common_file>": T("sudo vi %(common_file)s\n")
        , "suvimslap": T("sudo vi\n")
        , "emacs": T("emacs ")
        , "emacs <text>": T("emacs %(text)s") + K("tab,enter")        
        , "emaff <common_file>": T("emacs %(common_file)s\n")
        , "emacslap": T("emacs\n")
        , "sumacs": T("sudo emacs ")
        , "sumacs <text>": T("sudo emacs %(text)s") + K("tab,enter")        
        , "sumaff <common_file>": T("sudo emacs %(common_file)s\n")
        , "sumacslap": T("sudo emacs\n")
    }
    defaults = {
        "text":"",
        "text2":""
    }
    extras = [
        chc_base.text,
        chc_base.text2,
        chc_base.common_file,        
        chc_base.common_folder,
        chc_base.grep,
        chc_base.os_user
    ]
    
#---------------------------------------------------------------------------
# Git Rule
#---------------------------------------------------------------------------

class GitRule(MappingRule):
    mapping = {
        "git ": T("git ")
        , "git add": T("git add ")
        , "git add all": T("git add -A :/")
        , "git add all dir[ectory]": T("git add -A .")
        , "git add <text>": T("git add %(text)s") + K("tab:3")
        , "git initial commit": T('git commit -m "Initial commit.\n"')
        , "git commit": T('git commit -m ""') + K("left")
        , "git commit all": T('git commit -am ""') + K("left")
        , 'git amend': T("git commit --amend --no-edit\n")
        , 'git amend message': T("git commit --amend\n")
        , "git init": T("git init\n")
        , "git remote [show]": T("git remote -v\n")
        , "git remote add": T("git remote add ")
        , "git remote add <text>": T("git remote add %(text)s ")
        , "git remote add <text> partenza": T("git remote add %(text)s git@projects.partenza.de:")
        , "git remote add origin": T("git remote add origin git@projects.partenza.de:")
        , "git remote remove": T("git remote remove ")
        , "git push": T("git push\n")
        , "git push force": T("git push --force\n")
        , "git push upstream": T("git push -u ")
        , "git push origin master": T("git push -u origin master\n")
        , "git pull": T("git pull\n")
        , "git status": T("git status\n")
        , "git reset": T("git reset ")
        , "git reset <text>": T("git reset %(text)s") + K("tab:3")
        , "git reset head": T("git reset HEAD ")
        , "git reset head <text>": T("git reset HEAD %(text)s") + K("tab:3")
        , "git reset hard": T("git reset --hard ")
        , "git reset hard origin": T("git reset --hard origin/master")
        , "git reset hard head": T("git reset --hard HEAD")
        , "git branch": T("git branch ")
        , "git branch <text>": T("git branch %(text)s ")
        , "git branch move": T("git branch -m ")
        , "git branch delete": T("git branch -D ")
        , "git branch delete <text>": T("git branch -D %(text)s ")
        , "git branches": T("git branch -l\n")
        , "git clone": T("git clone ")
        , "git checkout": T("git checkout ")
        , "git checkout <text>": T("git checkout %(text)s\n")
        , "git checkout branch": T("git checkout -b ")
        , "git checkout branch <text>": T("git checkout -b %(text)s\n")
        , "git diff": T("git diff ")
        , "git diff head": T("git diff HEAD\n")
        , "git diff master": T("git diff master..")
        , "git diff <text>": T("git diff %(text)s ")
        , "git fetch": T("git fetch ")
        , "git fetch <text>": T("git fetch %(text)s ")
        , "git fetch origin": T("git fetch origin\n")
        , "git fetch upstream": T("git fetch upstream\n")
        , "git log": T("git log --stat \n")
        , "git log <1to100>": T("git log --stat -%(1to100)s\n")
        , "git log changes": T("git log -p \n")
        , "git log changes <1to100>": T("git log -p -%(1to100)s\n")
        , "git merge": T("git merge ")
        , "git merge <text>": T("git merge %(text)s")        
        , "git cherry pick": T("git cherry-pick ")
        , "git cherry pick abort": T("git cherry-pick --abort\n")
        , "git cherry pick continue": T("git cherry-pick --continue\n")
        , "git tag": T("git tag\n")
        , "git tag list": T("git tag -l ''") + K("left")
        , "git tag list <text>": T("git tag -l '%(text)s'") + K("left")
        , "git tag create": T("git tag -a v0.0 -m \"\"") + K("left")
        , "git tag create <text>": T("git tag -a vx -m \"%(text)s\"") + K("left")
        , "git tag delete": T("git tag -d")
        , "git tag push": T("git push --tags\n")
        , "git push tag[s]": T("git push --tags\n")
        , "git show": T("git show ")
        , "git show <text>": T("git show %(text)s ")
    }
    defaults = {
        "text":"",
        "1to100":"1"
    }
    extras = [
        chc_base.text,
        chc_base._1to100
    ]


#---------------------------------------------------------------------------
# IRC Rule
#---------------------------------------------------------------------------

class IrcRule(MappingRule):
    mapping = {
        "admin": T("/ADMIN\n")
        , "away": T("/AWAY ")
        , "away <text>": T("/AWAY %(text)s\n")
        , "away clear": T("/AWAY\n")
        , "channel help": T("/MSG ChanServ help ")
        , "channel help commands": T("/MSG ChanServ help\n")
        , "channel topic": T("/MSG ChanServ TOPIC ")
        , "channel topic append": T("/MSG ChanServ TOPICAPPEND ")
        , "channel topic prepend": T("/MSG ChanServ TOPICPREPEND ")
        , "help": T("/HELP\n")
        , "join": T("/j ")
        , "join <text>": T("/j %(text)s\n")
        , "knock": T("/KNOCK ")
        , "knock <text>": T("/KNOCK %(text)s\n")
        , "message": T("/MSG ")
        , "message <text>": T("/MSG %(text)s")
        , "nick": T("/NICK ")
        , "nick <text>": T("/NICK %(text)s\n")
        , "identify": T("/MSG NickServ identify ")
        , "quit": T("/QUIT\n")
        , "user stats": T("/LUSERS\n")
        , "who is": T("/WHOIS ")
        , "who is <text>": T("/WHOIS %(text)s\n")
    }
    defaults = {
        "text":""
    }
    extras = [
        chc_base.text
    ]
