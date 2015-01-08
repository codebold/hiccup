import unittest
import format as fmt

class FormatTest(unittest.TestCase):

    def test_camel_case(self):
        self.failUnless(fmt.camel_case("String formatting function") == "stringFormattingFunction")

    def test_pascal_case(self):
        self.failUnless(fmt.pascal_case("String formatting function") == "StringFormattingFunction")

    def test_capitalize(self):
        self.failUnless(fmt.capitalize("String formatting function") == "String Formatting Function")

    def test_upper_case(self):
        self.failUnless(fmt.upper_case("String formatting function") == "STRING FORMATTING FUNCTION")

    def test_lower_case(self):
        self.failUnless(fmt.lower_case("String formatting function") == "string formatting function")

    def test_sentence_case(self):
        self.failUnless(fmt.sentence_case("String formatting function") == "String formatting function")

    def test_snake_case(self):
        self.failUnless(fmt.snake_case("String formatting function") == "string_formatting_function")

    def test_screaming_snake_case(self):
        self.failUnless(fmt.screaming_snake_case("String formatting function") == "STRING_FORMATTING_FUNCTION")

    def test_lisp_case(self):
        self.failUnless(fmt.lisp_case("String formatting function") == "string-formatting-function")

    def test_screaming_lisp_case(self):
        self.failUnless(fmt.screaming_lisp_case("String formatting function") == "STRING-FORMATTING-FUNCTION")

    def test_train_case(self):
        self.failUnless(fmt.train_case("String formatting function") == "String-Formatting-Function")

    def test_no_spaces(self):
        self.failUnless(fmt.no_spaces("String formatting function") == "Stringformattingfunction")

    def test_upper_case_no_spaces(self):
        self.failUnless(fmt.upper_case_no_spaces("String formatting function") == "STRINGFORMATTINGFUNCTION")

    def test_lower_case_no_spaces(self):
        self.failUnless(fmt.lower_case_no_spaces("String formatting function") == "stringformattingfunction")

    def test_slashify(self):
        self.failUnless(fmt.slashify("String formatting function") == "String/formatting/function")

    def test_bashify(self):
        self.failUnless(fmt.bashify("String formatting function") == "String\\formatting\\function")

    def test_dotify(self):
        self.failUnless(fmt.dotify("String formatting function") == "String.formatting.function")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
