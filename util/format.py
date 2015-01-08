def camel_case(text):
    """Formats *text* in camel case.

    Args:
        text: the text to format
    Returns:
        the text in camel case

    >>> camel_case("String formatting function")
    stringFormattingFunction
    """
    words = str(text).lower().split(" ")
    return words[0] + "".join(w.capitalize() for w in words[1:])

def pascal_case(text):
    """Formats *text* in pasacal case.

    Args:
        text: the text to format
    Returns:
        the text in pascal case

    >>> pascal_case("String formatting function")
    StringFormattingFunction
    """
    words = [word.capitalize() for word in str(text).lower().split(" ")]
    return "".join(words)
    
def capitalize(text):
    """Capitalizes *text*.

    Args:
        text: the text to format
    Returns:
        the capitalized text

    >>> capitalize("String formatting function")
    String Formatting Function
    """
    words = [word.capitalize() for word in str(text).lower().split(" ")]
    return " ".join(words)

def upper_case(text):
    """Uppercases *text*.

    Args:
        text: the text to format
    Returns:
        the text in uppercase letters

    >>> upper_case("String formatting function")
    STRING FORMATTING FUNCTION
    """
    return str(text).upper()

def lower_case(text):
    """Downcases *text*.

    Args:
        text: the text to format
    Returns:
        the text in lowercase letters

    >>> lower_case("String formatting function")
    string formatting function
    """
    return str(text).lower()

def sentence_case(text):
    """Formats *text* in sentence case.

    Args:
        text: the text to format
    Returns:
        the text in sentence case

    >>> sentence_case("String formatting function")
    String formatting function
    """
    return str(text).capitalize()

def snake_case(text):
    """Formats *text* in snake case.

    Args:
        text: the text to format
    Returns:
        the text in snake case

    >>> snake_case("String formatting function")
    string_formatting_function
    """
    words = str(text).lower().split(" ")
    return "_".join(words)

def screaming_snake_case(text):
    """Formats *text* in screaming snake case.

    Args:
        text: the text to format
    Returns:
        the text in screaming snake case

    >>> screaming_snake_case("String formatting function")
    STRING_FORMATTING_FUNCTION
    """    
    words = str(text).upper().split(" ")
    return "_".join(words)

def lisp_case(text):
    """Formats *text* in lisp case.

    Args:
        text: the text to format
    Returns:
        the text in lisp case

    >>> lisp_case("String formatting function")
    string-formatting-function
    """
    words = str(text).lower().split(" ")
    return "-".join(words)

def screaming_lisp_case(text):
    """Formats *text* in screaming lisp case.

    Args:
        text: the text to format
    Returns:
        the text in screaming lisp case

    >>> screaming_lisp_case("String formatting function")
    STRING-FORMATTING-FUNCTION
    """
    words = str(text).upper().split(" ")
    return "-".join(words)

def train_case(text):
    """Formats *text* in train case.

    Args:
        text: the text to format
    Returns:
        the text in train case

    >>> train_case("String formatting function")
    String-Formatting-Function
    """
    words = [word.capitalize() for word in str(text).lower().split(" ")]
    return "-".join(words)

def no_spaces(text):
    """Removes all spaces from *text*.

    Args:
        text: the text to format
    Returns:
        the text without spaces

    >>> no_spaces("String formatting function")
    Stringformattingfunction
    """
    words = str(text).split(" ")
    return "".join(words)

def upper_case_no_spaces(text):
    """Removes all spaces and uppercases *text*.

    Args:
        text: the text to format
    Returns:
        the text without spaces in upper case

    >>> upper_case_no_spaces("String formatting function")
    STRINGFORMATTINGFUNCTION
    """
    words = str(text).upper().split(" ")
    return "".join(words)

def lower_case_no_spaces(text):
    """Removes all spaces and downcases *text*.

    Args:
        text: the text to format
    Returns:
        the text without spaces in lower case

    >>> lower_case_no_spaces("String formatting function")
    stringformattingfunction
    """
    words = str(text).lower().split(" ")
    return "".join(words)

def slashify(text):
    """Puts slashes between all words in *text*.

    Args:
        text: the text to format
    Returns:
        the words of text joined with slashes

    >>> slashify("String formatting function")
    String/formatting/function
    """
    words = str(text).split(" ")
    return "/".join(words)

def bashify(text):
    """Puts backslashes between all words in *text*.

    Args:
        text: the text to format
    Returns:
        the words of text joined with backslashes

    >>> bashify("String formatting function")
    String\formatting\function
    """
    words = str(text).split(" ")
    return "\\".join(words)

def dotify(text):
    """Puts dots hes between all words in *text*.

    Args:
        text: the text to format
    Returns:
        the words of text joined with dots

    >>> dotify("String formatting function")
    String.formatting.function
    """
    words = str(text).split(" ")
    return ".".join(words)
