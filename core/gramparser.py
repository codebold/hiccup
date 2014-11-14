# -*- coding: iso-8859-1 -*-
#
# Python Macro Language for Dragon NaturallySpeaking
#   (c) Copyright 1999 by Joel Gould
#   Portions (c) Copyright 1999 by Dragon Systems, Inc.
#
# gramparser.py
#   This module contains the Python code to convert the textual represenation
#   of a command and control grammar in the standard SAPI CFG binary format.
#
# April 1, 2000
#   - we now throw an exception if there is a bad parse instead of just
#     printing the error
#   - fixed a few minor bugs detecting errors
#

########################################################################
#
# Grammar format
# 
#   Rule Definition:
#       <RuleName> imported ;
#       <RuleName> = Expression ;
#       <RuleName> exported = Expression ;
#
#   A rule needs the keywork "exported" in order to be activated or visible
#   to other grammars for importing.
# 
#   Expression:
#       <RuleName>                  // no spaces
#       {ListName}                  // no spaces
#       Word
#       "Word"
#       ( Expression )
#       [ Expression ]              // optional
#       Expression +                // repeat
#       Expression Expression       // sequence
#       Expression | Expression     // alternative
#
# When building grammars there are three built in rules which can be imported:
#
#   <dgnletters>    Contains all the letters of the alphabet for spelling.
#       Letters are spelled like "a\\l", "b\\l", etc.
#
#   <dgnwords>      The set of all words active during dictation.
#
#   <dgndictation>  A special rule which corresponds to dictation.  It is
#       roughly equivelent to ( <dgnwords> | "\(noise)" )+  However, the
#       noise words is filtered out from any results reported to clients.
# 
########################################################################

from struct import pack
import re, sys, os, os.path, traceback
reAlphaNumeric = re.compile('\w+$')
#
# This is the lexical scanner.
#
# We take a list of strings as input (such as would be returned by readlines).
#
# After every call to getAnotherToken or testAndEatToken the variables token
# and value will contain the details about the next token in the input stream.
#

import string, pprint, copy

class GrammarParserError(Exception):
    """these exceptions all expect the scanObj as second parameter
    in order to produce the correct message info
    """
    def __init__(self, message, scanObj):
        self.message = message
        self.scanObj = scanObj
        
    def __str__(self):
        """return special info for scanner or parser exceptions.
        """
        gramName = self.scanObj.grammarName or ""
        L = []
        if self.scanObj.phase == 'scanning':
            line = self.scanObj.line + 1
            startPos, charPos = self.scanObj.start+1, self.scanObj.char+1
            if startPos == charPos:
                pos = charPos
            elif charPos - startPos == 1:
                pos = charPos
            else:
                pos = '%s-%s'% (startPos, charPos)
            errorMarker = self.scanObj.getError()
            if gramName:
                L.append('in grammar "%s", line %s, position %s:'% (gramName, line, pos))
            else:
                L.append('in grammar, line %s, position %s:'% (line, pos))
            L.append(self.message)
            L.append(errorMarker)
        else:
            if gramName:
                L.append('in grammar "%s", %s scanning/parsing:'% (gramName, self.scanObj.phase))
            else:
                L.append('in grammar, %s scanning/parsing:'% self.scanObj.phase)
            L.append(self.message)
        
        L.append(self.dumpToFile())
            
        return '\n'.join(L)
        
    def dumpToFile(self):
        """dump grammar and traceback to a file for debugging purposes
        """
        gramName = self.scanObj.grammarName
        dirName = os.path.dirname(__file__)
        if gramName:
            filename = 'error_info_grammar_%s.txt'% gramName
        else:
            filename = 'error_info_natlink_grammar.txt'
        filepath = os.path.join(dirName, filename)
        L = []
        if gramName:
            L.append('Info about scanner/parser error of NatLink grammar "%s"\n'% gramName)
        else:
            L.append('Info about scanner/parser error of NatLink grammar\n')
        
        tbstr = '\n'.join(traceback.format_exc().split('\n')[:-2])
        L.append(tbstr)

        L.append('\nThe complete grammar:\n')
        if self.scanObj.phase == 'scanning':
            for i, line in enumerate(self.scanObj.text):
                if i == self.scanObj.line:
                    L.append(self.scanObj.getError())
                elif i == len(self.scanObj.text)-1 and not line.strip():
                    L.append("%.2s: %s"% (i+1, line))

        else:
            L.extend(self.scanObj.text)
        L.append('')

        try:
            open(filepath, 'w').write('\n'.join(L))
            return '(more info in file: %s)'% filepath
        except IOError, message:
            return '(could not write more info to error file %s (%s))'% (filepath, message)
                         
class SyntaxError(GrammarParserError):
    pass

class LexicalError(GrammarParserError):
    pass


class SymbolError(GrammarParserError):
    pass

class GrammarError(GrammarParserError):
    pass

SeqCode = 1     # sequence
AltCode = 2     # alternative
RepCode = 3     # repeat
OptCode = 4     # optional

class GramScanner(object):

    def __init__(self,text=None, grammarName=None):
        self.token = None
        self.value = None
        self.line = 0;
        self.char = 0;
        if text:
            self.text = copy.copy(text)
            if self.text[-1] != '\0':
                self.text.append('\0')
        else:
            self.text = ['\0']
        self.lastWhiteSpace = ""  # for gramscannerreverse
        self.grammarName = grammarName or ""
        self.phase = "before"
    
    def newText(self,text):
        GramScanner.__init__(self, text);

    def getError(self):
        if self.token == '\0' or self.text[self.line][0] == '\0':
            errorLine = '=> (end of input)\n'
        else:
            spacing = ' '*self.start
            hats = '^' * (self.char - self.start)
            if not hats:
                hats = '^'
            errorLine = '=> '+self.text[self.line]+'\n=> '+spacing + hats + '\n'
        return errorLine

    def testAndEatToken(self, token):
        if self.token != token:
            raise SyntaxError( "expecting '%s'" % token, self )
        else:
            value = self.value
            self.getAnotherToken()
            return value

    def skipWhiteSpace(self):
        """skip whitespace and comments, but keeps the leading comment/whitespace
        in variable self.lastWhiteSpace (QH, july 2012)
        """
        ch = self.char
        oldPos = ch
        oldLine = self.line
        while 1:
            ln = self.text[self.line]
            lnLen = len(ln)
            while ch < lnLen and ln[ch] in string.whitespace:
                ch = ch + 1
            if ch < lnLen and ln[ch] != '#':
                break
            self.line = self.line + 1
            self.text[self.line] = string.replace(self.text[self.line],'\t',' ')
            self.text[self.line] = string.replace(self.text[self.line],'\n',' ')
            ch = 0
        self.char = ch
        if self.line == oldLine:
            self.lastWhiteSpace = ln[oldPos:ch]
        else:
            L = [self.text[oldLine][oldPos:]]
            for l in range(oldLine+1, self.line):
                L.append(self.text[l])
            L.append(self.text[self.line][:ch])
            self.lastWhiteSpace = '\n'.join(L)
                

    def getAnotherToken(self):
        """return a token and (if appropriate) the corresponding value
        
        token can be '=', '|', '+', ';', '(', ')', '[', ']' (with value None)
        or 'list' (value without {})
        or 'rule' (value wihtout <>)
        or 'sqword', 'dqword', 'word'  (a word, in single quotes, double quotes or unquoted)
        Note "exorted" and "imported" and list names and rule names must have token 'word'
        Grammar words can have dqword or sqword too. (dqword and sqword added by QH, july 2012)
        
        """    
    
        if self.token == '\0':
            return None
        
        self.value = None

        self.skipWhiteSpace()  # now leaves self.lastWhiteSpace
        ch = self.char
        ln = self.text[self.line]
        lnLen = len(ln)

        self.start = ch
        
        if ln[ch] in ['(', ')', '[', ']', '|', '+', '=', ';', '\0']:
            self.token = ln[ch]
            ch = ch + 1

        elif ln[ch] == '"':
            self.token = 'dqword'
            ch = ch + 1
            while ch < lnLen and ln[ch] != '"':
                ch = ch + 1
            if ch >= lnLen:
                raise LexicalError( "expecting closing quote in word name", self)
            self.value = ln[self.start+1:ch]
            ch = ch + 1
        
        elif ln[ch] == "'":
            self.token = 'sqword'
            ch = ch + 1
            while ch < lnLen and ln[ch] != "'":
                ch = ch + 1
            if ch >= lnLen:
                raise LexicalError( "expecting closing quote in word name", self)
            self.value = ln[self.start+1:ch]
            ch = ch + 1
        
        elif ln[ch] == '<':
            self.token = 'rule'
            ch = ch + 1
            while ch < lnLen and ln[ch] != '>':
                ch = ch + 1
            if ch >= lnLen:
                raise LexicalError( "expecting closing angle bracket in rule name", self)
            self.value = ln[self.start+1:ch]
            ch = ch + 1

        elif ln[ch] == '{':
            self.token = 'list'
            ch = ch + 1
            while ch < lnLen and ln[ch] != '}':
                ch = ch + 1
            if ch >= lnLen:
                raise LexicalError( "expecting closing brace in list name", self)
            self.value = ln[self.start+1:ch]
            ch = ch + 1

        elif isCharOrDigit(ln[ch]):
            self.token = 'word'
            while ch < lnLen and isCharOrDigit(ln[ch]):
                ch = ch + 1
            self.value = ln[self.start:ch]

        else:
            raise LexicalError( "unknown character found", self)

        self.char = ch

## generator function, scanning the tokens and whitespace of a gramspec:
## this class can scan a grammar, return the tokens in a generator function
## and put back the results exactly the same:
class GramScannerReverse(GramScanner):
    def __init__(self, text=None):
        GramScanner.__init__(self, text)
        self.returnList = []        
            
    def gramscannergen(self):
        """this generator function gives all whitespace, token, value tuples
        
        end with (whitespace, '\0', None)
        """
        while 1:
            newToken = self.getAnotherToken()
            token = self.token
            if token == '\0':
                yield self.lastWhiteSpace.rstrip('\n'), '\0', None
                return
            value = self.value
            whitespace = self.lastWhiteSpace
            yield whitespace, token, value

    def appendToReturnList(self, whitespace, token, value):
        """add to the returnList, to produce equal result or translation
        """
        L = self.returnList
        if whitespace:
            L.append(whitespace)
        if token == '\0':
            return
        
        if token == 'rule':
            L.append('<%s>'% value)
        elif token == 'list':
            L.append('{%s}'% value)
        elif token == 'word':
            if reAlphaNumeric.match(value):
                L.append(value)
            elif "'" in value:
                L.append('"%s"'% value)
            else :
                L.append("'%s'"% value)
        elif token == 'sqword':
            L.append("'%s'"% value)
        elif token == 'dqword':
            L.append('"%s"'% value)
        elif value is None:
            L.append(token)
        else:
            L.append(value)
    
    def mergeReturnList(self):
        return ''.join(self.returnList)

class peek_ahead(object):
    """Iterator that can look ahead one step

    From example 16.7 from python cookbook 2.

    The preview can be inspected through it.preview
    
    Here used for the gramscannergen in GramScannerReverse

    #ignoring duplicates:
    #>>> it = peek_ahead('122345567')
    #>>> for i in it:
    #...     if it.preview == i:
    #...         continue
    #...     print i,
    #1 2 3 4 5 6 7

    """
    sentinel = object() #schildwacht
    def __init__(self, it):
        self._nit = iter(it).next
        self.preview = None
        self.previous = None
        self.current = None
        self._step()
    def __iter__(self):
        return self
    def next(self):
        self.previous = self.current
        result = self._step()
        if result is self.sentinel: raise StopIteration
        else:
            self.current = result
            return result
    def _step(self):
        self.current = self.preview
        try: self.preview = self._nit()
        except StopIteration: self.preview = self.sentinel
        return self.current
        
#
# This is a rule parser.  It builds up data structures which contain details
# about the rules in the parsed text.
#
# The definition of a rule is an array which contains tuples.  The array 
# contains the rule elements in sequence.  The tuples are pairs of element
# type and element value
#

class GramParser(object):

    def __init__(self,text=[''], grammarName=None):
        self.scanObj = GramScanner(text, grammarName=grammarName)
        self.knownRules = {}
        self.knownWords = {}
        self.knownLists = {}
        self.nextRule = 1
        self.nextWord = 1
        self.nextList = 1
        self.exportRules = {}
        self.importRules = {}
        self.ruleDefines = {}
        self.grammarName = grammarName or ""

    def doParse(self,*text):
        self.scanObj.phase = "scanning"
        if text:
            self.scanObj.newText(text[0])
        #try:
        self.scanObj.getAnotherToken()
        while self.scanObj.token != '\0':
            self.parseRule()
        self.scanObj.phase = "after"
        #except SyntaxError, message:
        #    raise SyntaxError("Syntax error at column: %d\n%s\n"%(self.scanObj.start,message)+self.scanObj.getError())
        #except LexicalError, message:
        #    raise LexicalError("Lexical error at column: %d\n%s\n"%(self.scanObj.start,message)+self.scanObj.getError())
        #except SymbolError, message:
        #    raise SymbolError("Symbol error at column: %d\n%s\n"%(self.scanObj.start,message)+self.scanObj.getError())

    def parseRule(self):
        if self.scanObj.token != 'rule':
            raise SyntaxError("expecting rule name to start rule definition", self.scanObj)
        ruleName = self.scanObj.value
        if not isValidListOrRulename(ruleName):
            raise SyntaxError('rulename may may only contain ascii letters, digits or - or _: "%s"'% ruleName, self.scanObj)
        if self.ruleDefines.has_key(ruleName):
            raise SymbolError( "rule '%s' has already been defined" % ruleName, self.scanObj)
        if self.importRules.has_key(ruleName):
            raise SymbolError( "rule '%s' has already been defined as imported" % ruleName, self.scanObj)
        if self.knownRules.has_key(ruleName):
            ruleNumber = self.knownRules[ruleName]
        else:
            ruleNumber = self.nextRule
            self.nextRule = self.nextRule + 1
            self.knownRules[ruleName] = ruleNumber
        self.scanObj.getAnotherToken()
        if self.scanObj.token == 'word' and self.scanObj.value == 'imported':
            self.importRules[ruleName] = ruleNumber
            self.scanObj.getAnotherToken()
        else:
            if self.scanObj.token == 'word' and self.scanObj.value == 'exported':
                self.exportRules[ruleName] = ruleNumber
                self.scanObj.getAnotherToken()
            self.scanObj.testAndEatToken('=')
            self.ruleDefines[ruleName] = self.parseExpr()
        self.scanObj.testAndEatToken(';')

    def parseExpr(self):
        definition = []
        moreThanOne = 0
        while 1:
            definition = definition + self.parseExpr2()
            if self.scanObj.token != '|':
                break
            self.scanObj.getAnotherToken()
            moreThanOne = 1
        if moreThanOne:
            return [ ('start', AltCode) ] + definition + [ ('end', AltCode) ]
        else:
            return definition

    def parseExpr2(self):
        definition = []
        moreThanOne = 0
        while 1:
            definition = definition + self.parseExpr3()
            if self.scanObj.token not in ( 'word', 'sqword', 'dqword', 'rule', 'list', '(', '[' ):
                break
            moreThanOne = 1
        if moreThanOne:
            return [ ('start', SeqCode) ] + definition + [ ('end', SeqCode) ]
        else:
            return definition

    def parseExpr3(self):
        definition = self.parseExpr4()
        if self.scanObj.token == '+':
            self.scanObj.getAnotherToken()
            return [ ('start', RepCode) ] + definition + [ ('end', RepCode) ]
        else:
            return definition

    def parseExpr4(self):
        if self.scanObj.token in ['word', 'sqword', 'dqword']:
            wordName = self.scanObj.value
            if not wordName:
                raise SyntaxError("empty word name", self.scanObj)
            if self.knownWords.has_key(wordName):
                wordNumber = self.knownWords[wordName]
            else:
                wordNumber = self.nextWord
                self.nextWord = self.nextWord + 1
                self.knownWords[wordName] = wordNumber
            self.scanObj.getAnotherToken()
            return [ ( 'word', wordNumber ) ]
                
        elif self.scanObj.token == 'list':
            listName = self.scanObj.value
            if not listName:
                raise SyntaxError("empty word name", self.scanObj)
            if not isValidListOrRulename(listName):
                raise SyntaxError('listname may may only contain ascii letters, digits or - or _: "%s"'% listName, self.scanObj)
            if self.knownLists.has_key(listName):
                listNumber = self.knownLists[listName]
            else:
                listNumber = self.nextList
                self.nextList = self.nextList + 1
                self.knownLists[listName] = listNumber
            self.scanObj.getAnotherToken()
            return [ ( 'list', listNumber ) ]
                
        elif self.scanObj.token == 'rule':
            ruleName = self.scanObj.value
            if not ruleName:
                raise SyntaxError("empty word name", self.scanObj)
            if not isValidListOrRulename(ruleName):
                raise SyntaxError('rulename may may only contain ascii letters, digits or - or _: "%s"'% ruleName, self.scanObj)
            if self.knownRules.has_key(ruleName):
                ruleNumber = self.knownRules[ruleName]
            else:
                ruleNumber = self.nextRule
                self.nextRule = self.nextRule + 1
                self.knownRules[ruleName] = ruleNumber
            self.scanObj.getAnotherToken()
            return [ ( 'rule', ruleNumber ) ]
                
        elif self.scanObj.token == '(':
            self.scanObj.getAnotherToken()
            definition = self.parseExpr()
            self.scanObj.testAndEatToken(')')
            return definition

        elif self.scanObj.token == '[':
            self.scanObj.getAnotherToken()
            definition = self.parseExpr()
            self.scanObj.testAndEatToken(']')
            #self.reportOptionalRule(definition)
            return [ ('start', OptCode) ] + definition + [ ('end', OptCode) ]

        else:
            raise SyntaxError( "expecting expression (word, rule, etc.)", self.scanObj)

    def reportOptionalRule(self, definition):
        """print the words that are optional, for testing BestMatch V"""
        wordsRev = dict([(v,k) for k,v in self.knownWords.items()])

        for w, number in definition:
            if w == 'word':
                print 'optional word: %s'% wordsRev[number]

    def checkForErrors(self):
        if not len(self.exportRules):
            raise GrammarError( "no rules were exported", self.scanObj)
        for ruleName in self.knownRules.keys():
            if not self.importRules.has_key(ruleName) and not self.ruleDefines.has_key(ruleName):
                raise GrammarError( "rule '%s' was not defined or imported" % ruleName, self.scanObj)

    def dumpString(self):
        """returns the parts that are non empty
        """
        L = []
        for name in ["knownRules", "knownLists", "knownWords",
                    "exportRules","importRules" , "ruleDefines" ]:
            var = getattr(self, name)
            if var:
                L.append(name + ":")
                L.append(pprint.pformat(var))
        return '\n'.join(L)

    def dumpStringNice(self):
        """returns the parts that are non empty
        reverse numbers of rules and ruleDefines... must be identical in gramparserlexyacc...
        """
        L = []
        rulesRev = dict([(v,k) for k,v in self.knownRules.items()])
        wordsRev = dict([(v,k) for k,v in self.knownWords.items()])
        listsRev = dict([(v,k) for k,v in self.knownLists.items()])
        codeRev = {SeqCode:'SeqCode',
                   AltCode:'AltCode',
                   RepCode:'RepCode',
                   OptCode:'OptCode'}
    
        for name in ["exportRules","importRules"]:
            var = getattr(self, name)
            if var:
                L.append('%s: %s'% (name, ', '.join(var)))
        if self.ruleDefines:
            ruleDefinesNice = dict([(rulename, [self.nicenItem(item, rulesRev, wordsRev, listsRev,codeRev) \
                                                for item in ruleList]) \
                                     for (rulename,ruleList) in self.ruleDefines.items()])
                                    
            L.append(pprint.pformat(ruleDefinesNice))
        return '\n'.join(L)

    def dumpNice(self):
        """returns the parts that are non empty
        return a dict, with keys
        knownRules, knownWords, exportRules, ruleDefines, importRules (if not empty)

        reverse numbers of rules and ruleDefines... must be identical in gramparserlexyacc...
        """
        D = {}
        rulesRev = dict([(v,k) for k,v in self.knownRules.items()])
        wordsRev = dict([(v,k) for k,v in self.knownWords.items()])
        listsRev = dict([(v,k) for k,v in self.knownLists.items()])
        codeRev = {SeqCode:'SeqCode',
                   AltCode:'AltCode',
                   RepCode:'RepCode',
                   OptCode:'OptCode'}
    
        for name in ["exportRules","importRules"]:
            var = getattr(self, name)
            if var:
                D[name] = var.keys()
        if self.ruleDefines:
            ruleDefinesNice = dict([(rulename, [self.nicenItem(item, rulesRev, wordsRev, listsRev,codeRev) \
                                                for item in ruleList]) \
                                     for (rulename,ruleList) in self.ruleDefines.items()])
            D['ruleDefines'] = ruleDefinesNice       
        return D

    def nicenItem(self, item, rulesRev, wordsRev, listsRev, codeRev):
        i,v = item
        if i == 'word':
            return (i, wordsRev[v])
        elif i == 'list':
            return (i, listsRev[v])
        elif i == 'rule':
            return (i, rulesRev[v])
        elif i in ('start', 'end'):
            return (i, codeRev[v])
        else:
            raise ValueError('invalid item in nicenItem: %s'% i)

    def dumpContents(self):
        print "Dumping GramParser object..."
        print "  knownRules:"
        for name in self.knownRules.keys():
            print "    ", name, self.knownRules[name]
        print "  knownLists:"
        for name in self.knownLists.keys():
            print "    ", name, self.knownLists[name]
        print "  knownWords:"
        for name in self.knownWords.keys():
            print "    ", name, self.knownWords[name]
        print "  exportRules:"
        for name in self.exportRules.keys():
            print "    ", name, self.exportRules[name]
        print "  importRules:"
        for name in self.importRules.keys():
            print "    ", name, self.importRules[name]
        print "  ruleDefines:"
        for name in self.ruleDefines.keys():
            print "    ", name
            for element in self.ruleDefines[name]:
                print "      ", element[0], element[1]

#
# This function takes a GramParser class which contains the parse of a grammar
# and returns a "string" object which contains the binary representation of
# that grammar.
#
# The binary form is standard SAPI which consists a header followed by five
# "chunks".  The first four chunks are all in the same format and are lists
# of the names and number of the exported rules, imported rules, lists and
# words respectively.
#
# The fifth chunk contains the details of the elements which make up each
# defined rule.
#

def packGrammar(parseObj):
    output = ""

    # header:
    #   DWORD dwType  = 0
    #   DWORD dwFlags = 0
    output = output + pack("LL", 0, 0)

    # various chunks
    if len(parseObj.exportRules):
        output = output + packGrammarChunk(4, parseObj.exportRules)
    if len(parseObj.importRules):
        output = output + packGrammarChunk(5, parseObj.importRules)
    if len(parseObj.knownLists):
        output = output + packGrammarChunk(6, parseObj.knownLists)
    if len(parseObj.knownWords):
        output = output + packGrammarChunk(2, parseObj.knownWords)
    if len(parseObj.ruleDefines):
        output = output + packGrammarRules(3, parseObj.knownRules, parseObj.ruleDefines)
    return output


def packGrammarChunk(type,dict):
    output = ""
    totalLen = 0

    for word in dict.keys():
        # chunk data entry
        #   DWORD dwSize = number of bytes in entry
        #   DWORD dwNum  = ID number for this rule/word
        #   DWORD szName = name of rule/word, zero-term'd and padded to dword
        paddedLen = ( len(word) + 4 ) & 0xFFFC
        output = output + pack( "LL%ds" % paddedLen, paddedLen+8, dict[word], word )
        totalLen = totalLen + paddedLen+8

    # chunk header
    #   DWORD dwChunkID = type
    #   DWORD dwChunkSize = number of bytes in chunk not including this header
    return pack( "LL", type, totalLen ) + output


def packGrammarRules(type,names,dict):
    output = ""
    totalLen = 0
    elemType = { 'start':1, 'end':2, 'word':3, 'rule':4, 'list':6 }

    for word in dict.keys():
        ruleDef = ""
        ruleLen = 0

        for element in dict[word]:
            # repeated element:
            #   WORD wType    = element type
            #   WORD wProb    = 0
            #   DWORD dwValue = element value
            ruleDef = ruleDef + pack( "HHL", elemType[element[0]], 0, element[1] )
            ruleLen = ruleLen + 8
        
        # rule definition:
        #   DWORD dwSize = number of bytes in rule definition
        #   DWORD dwnum  = ID number of rule
        output = output + pack( "LL", ruleLen+8, names[word] ) + ruleDef
        totalLen = totalLen + ruleLen+8

    # chunk header:
    #   DWORD dwChunkID = type
    #   DWORD dwChunkSize = number of bytes in chunk not including this header
    return pack( "LL", type, totalLen ) + output

#
# This is a routine which was included for testing but can also be used to 
# compile grammar files.  It takes an input file name containing a grammar 
# and an output file name to write the binary into.
#

def parseGrammarAndSave(inName,outName):
    inFile = open(inName,'r')
    parseObj = GramParser()
    parseObj.doParse( inFile.readlines() )
    inFile.close()
    binary = gramparser.packGrammar(parseObj)
    outFile = open(outName,'wb')
    outFile.write( binary )
    outFile.write( "hello" )
    outFile.close()

def isCharOrDigit(ch):
    """test if ch is in string.letters, or in string.digits, or an acuted char
    
    this is for the gramparser, which can contain words for the recogniser
    
    acuted is with ascii value (ord) >= 192
    """
    if ch in string.letters:
        return 1
    if ch in string.digits:
        return 1
    if ord(ch) >= 192:
        return 1
    # else false

def isValidListOrRulename(word):
    """test if there are no accented characters in a listname or rulename
    
    so asciiletters, digitis, - and _ are allowed
    """
    allowed = string.ascii_letters + string.digits + '-_'
    if not word:
        return
    for w in word:
        if not w in allowed:
            return
    # passed:
    return 1

#
# This utility routine will split apart strings at linefeeds in a list of
# strings.  For example:
#
#   [ "This is line one\nThis is line two", "This is line three" ]
#
# Becomes:
#
#   [ "This is line one\n", "This is line two", "This is line three" ]
#

#def splitApartLines(lines):
#    x = 0
#    while x < len(lines):
#        crlf = string.find(lines[x],'\n')
#        if crlf >= 0:
#            lines[x:x+1] = [ lines[x][:crlf+1], lines[x][crlf+1:] ] 
#        x = x + 1
def splitApartLines(lines):
    """split apart the lines of a grammar and clean up unwanted spacing
    
    see  unittest still problems here!!
    """
    for x in range(len(lines)-1, -1, -1):
        lines[x] = lines[x].rstrip()
        crlf = lines[x].find('\n')
        if crlf >= 0:
            lines[x:x+1] = lines[x].split('\n')

    # spacing at end of lines:
    for i, line in enumerate(lines):
        if line != line.rstrip():
            lines[i] = line.rstrip()

    leftSpacing = [len(l) - len(l.lstrip()) for l in lines]
    if len(leftSpacing) == 0:
        raise ValueError("splitApartLines, empyt grammar: %s"% repr(lines))

    if len(leftSpacing) > 1:
        minLeftSpacing = min(leftSpacing[1:])
    for i, line in enumerate(lines):
        if i == 0:
            if line != line.lstrip():
                lines[i] = line.lstrip()
        else:
            if minLeftSpacing:
                lines[i] = line[minLeftSpacing:]
        


test = """
>>> gramSpec = ['<rule> exported = action;']
>>> parser = GramParser(gramSpec)
>>> parser.doParse()
>>> parser.checkForErrors()
>>> print parser.dumpString()
knownRules: 
{'rule': 1}
knownWords: 
{'action': 1}
exportRules: 
{'rule': 1}
ruleDefines: 
{'rule': [('word', 1)]}

"""

###doctest handling:
__test__ = dict(test = test
                )
def _test():
    import doctest, gramparser
    reload(gramparser)
    
    doctest.master = None
    return  doctest.testmod(gramparser)
            
if __name__ == "__main__":
    _test()

