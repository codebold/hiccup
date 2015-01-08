import re

from dragonfly import (
    Keyboard,
    Text
)

import util.format as fmt

class PunctuatedText(Text):

    def __init__(self, spec=None, static=False, pause=0.00001, autofmt=False, correct_punctuations=True):
        self._correct_punctuations = correct_punctuations
            
        super(PunctuatedText, self).__init__(spec, static, pause, autofmt)

    def _execute(self, data=None):
        if not self._static and data:
            print data

            if "text" in data:
                for part in data["text"]._words:
                    print part

        super(PunctuatedText, self)._execute(data)
   
    def _old_parse_spec(self, spec):
        if self._correct_punctuations:
            spec = self._correct_punctuation_marks(spec)

        return super(PunctuatedText, self)._parse_spec(spec)

    def _correct_punctuation_marks(self, spec):       
        parts = re.split("\%\([a-z_0-9]+\)s", self._spec)
            
        if len(parts) > 2:
            raise Exception("PunctuatedText only supports one variable, yet.")
                
        start = len(parts[0])
        end = len(spec) - len(parts[1])
        words = spec[start:end]
        words = self._strip_punctuation_info(words)
        newText = ""
            
        for word in words:
            if (newText != "" and newText[-1:].isalnum() and word[-1:].isalnum()):
                word = " " + word # Adds spacing between normal words.                    
            newText += word
            
        return parts[0] + newText + parts[1]

    def _strip_punctuation_info(text):
        newWords = []
        words = str(text).split(" ")
        for word in words:
            if word.startswith("\\backslash"):
                word = "\\" # Backslash requires special handling.
            elif word.find("\\") > -1:
                word = word[:word.find("\\")] # Remove spoken form info.
            newWords.append(word)
        return newWords
        

class FormattedText(Text):

    _format = staticmethod(str)

    def __init__(self, spec=None, static=False, pause=0.00001, autofmt=False, format=None):
        if format is None: format = self._format
        
        self._format = format
            
        super(FormattedText, self).__init__(spec, static, pause, autofmt)

    def _parse_spec(self, spec):
        if self._format:
            spec = self._format(spec)

        return super(FormattedText, self)._parse_spec(spec)

    
class CamelCase(FormattedText):
    _format = staticmethod(fmt.camel_case)

class PascalCase(FormattedText):
    _format = staticmethod(fmt.pascal_case)

class Capitalize(FormattedText):
    _format = staticmethod(fmt.capitalize)

class UpperCase(FormattedText):
    _format = staticmethod(fmt.upper_case)

class LowerCase(FormattedText):
    _format = staticmethod(fmt.lower_case)

class SentenceCase(FormattedText):
    _format = staticmethod(fmt.sentence_case)

class SnakeCase(FormattedText):
    _format = staticmethod(fmt.snake_case)

class ScreamingSnakeCase(FormattedText):
    _format = staticmethod(fmt.screaming_snake_case)

class LispCase(FormattedText):
    _format = staticmethod(fmt.lisp_case)

class ScreamingLispCase(FormattedText):
    _format = staticmethod(fmt.screaming_lisp_case)

class TrainCase(FormattedText):
    _format = staticmethod(fmt.train_case)

class NoSpaces(FormattedText):
    _format = staticmethod(fmt.no_spaces)

class UpperCaseNoSpaces(FormattedText):
    _format = staticmethod(fmt.upper_case_no_spaces)

class LowerCaseNoSpaces(FormattedText):
    _format = staticmethod(fmt.lower_case_no_spaces)

class Slashify(FormattedText):
    _format = staticmethod(fmt.slashify)

class Bashify(FormattedText):
    _format = staticmethod(fmt.bashify)

class Dotify(FormattedText):
    _format = staticmethod(fmt.dotify)
