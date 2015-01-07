import re

from dragonfly import (
    ActionBase,
    DynStrActionBase,
    Keyboard,
    IntegerRef,
    typeables
)

class RepeatedText(DynStrActionBase):


    _pause = 0.00001
    _keyboard = Keyboard()
    _specials = {
        "\n":   typeables["enter"],
        "\t":   typeables["tab"],
    }
    _repeat = 1

    def __init__(self, spec=None, static=False, pause=None,
                 autofmt=False):
        super(RepeatedText, self).__init__(spec, static)
        if not pause:
            pause = self._pause
        self._pause = pause
        self._autofmt = autofmt

    def _parse_spec(self, spec):
        if not self._static:
            ref_match = re.search(":%\\(([\\w]+)\\)[ds]{1}$", self._spec)
            value_match = re.search(":([\\d]+)$", spec)
            
            if (ref_match.group() and value_match.group):               
                ref = ref_match.group(1)
                value = value_match.group(1)
                
                self._repeat = int(value)
                spec = spec[:-(len(value) + 1)]
                
        events = []
        for character in spec:
            if character in self._specials:
                typeable = self._specials[character]
            else:
                try:
                    typeable = Keyboard.get_typeable(character)
                except ValueError, e:
                    raise ActionError("Keyboard interface cannot type this"
                                      " character: %r (in %r)"
                                      % (character, spec))
            events.extend(typeable.events(self._pause))
        return events

    def _execute(self, data=None):
        if self._static:
            # If static, the events have already been parsed by the
            #  initialize() method.
            self._execute_repeated_events(self._events)

        else:
            # If not static, now is the time to build the dynamic spec,
            #  parse it, and execute the events.

            if not data:
                spec = self._spec
            else:
                try:
                    spec = self._spec % data
                except KeyError:
                    self._log_exec.error("%s: Spec %r doesn't match data %r."
                                         % (self, self._spec, data))
                    return False

            self._log_exec.debug("%s: Parsing dynamic spec: %r"
                                 % (self, spec))
            events = self._parse_spec(spec)
            self._execute_repeated_events(events)

    def _execute_repeated_events(self, events):
        for i in range(self._repeat):
            self._execute_events(events)

    def _execute_events(self, events):
        """
            Send keyboard events.

            If instance was initialized with *autofmt* True,
            then this method will mimic a word recognition
            and analyze its formatting so as to autoformat
            the text's spacing and capitalization before
            sending it as keyboard events.

        """

        if self._autofmt:
            # Mimic a word, select and copy it to retrieve capitalization.
            get_engine().mimic("test")
            Key("cs-left, c-c/5").execute()
            word = Clipboard.get_text()

            # Inspect formatting of the mimicked word.
            index = word.find("test")
            if index == -1:
                index = word.find("Test")
                capitalize = True
                if index == -1:
                    self._log.error("Failed to autoformat.")
                    return False
            else:
                capitalize = False

            # Capitalize given text if necessary.
            text = self._spec
            if capitalize:
                text = text[0].capitalize() + text[1:]

            # Reconstruct autoformatted output and convert it
            #  to keyboard events.
            prefix = word[:index]
            suffix = word[index + 4:]
            events = self._parse_spec(prefix + text + suffix)

        # Send keyboard events.
        self._keyboard.send_keyboard_events(events)
        return True

        
class ExtensibleRepeatedText(RepeatedText):

    def __init__(self, spec=None, static=False, pause=None,
                 autofmt=False):
        super(ExtensibleRepeatedText, self).__init__(spec, static, pause, autofmt)

    def _execute_events(self, events):
        """ Execute prolog, send keyboard events and executes the epilog. """
        self._execute_before_keyboard_events()
        super(ExtensibleRepeatedText, self)._keyboard.send_keyboard_events(events)
        self._execute_after_keyboard_events()
        return True

    def _execute_before_keyboard_events(self):
        """ Virtual method. """

    def _execute_after_keyboard_events(self):
        """ Virtual method. """


class ActionSeries(ActionBase):

    #-----------------------------------------------------------------------
    # Initialization methods.

    def __init__(self, *actions):
        ActionBase.__init__(self)
        self._actions = list(actions)
        self._str = ", ".join(str(a) for a in actions)

    def append(self, other):
        assert isinstance(other, ActionBase)
        self._actions.append(other)
        self._str = ", ".join(str(a) for a in self._actions)

    def __iadd__(self, other):
        self.append(other)
        return self

    #-----------------------------------------------------------------------
    # Execution methods.

    def execute(self, data=None):
        for action in self._actions:
            action.execute(data)
