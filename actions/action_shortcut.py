from dragonfly import (
    Text,
    Key,
    Pause,
    Mouse
)

#---------------------------------------------------------------------------
# Shortcuts
#---------------------------------------------------------------------------

def T(s, pause=0.00001, **kws):
    return Text(s, pause=pause, **kws)

def K(*args, **kws):
    return Key(*args, **kws)

def P(*args, **kws):
    return Pause(*args, **kws)

def M(*args, **kws):
    return Mouse(*args, **kws)
