#!/usr/bin/env python
import unittest
import argument_parser

class TestArgumentParser(unittest.TestCase):
    def test_read(self):
        options_without_arguments = ['A', 'a', '1']
        options_with_arguments = ['B', 'b', '2']
        argv = ['test.py', '-A', 'operand_1', '-B', 'b_option_argument', '-1', 'operand_2', '--', '-A', 'operand_4']
        correct_option_values = {'A': None, 'B': 'b_option_argument', '1': None}
        correct_operands = ['operand_1', 'operand_2', '-A', 'operand_4']
        correct_result = (correct_option_values, correct_operands)
        self.assertEqual(argument_parser.read(argv, options_without_arguments, options_with_arguments), correct_result)
    


    def test_make_option_dict(self):
        #two same options in a
        a = ['a', 'a']
        b = ['c', 'd', 'e']
        self.assertRaises(ValueError, argument_parser.make_option_dict, a, b)

        #two same options in b
        a = ['a', 'b']
        b = ['c', 'c']
        self.assertRaises(ValueError, argument_parser.make_option_dict, a, b)
        #same option in a and b
        a = ['a', 'b']
        b = ['a', 'c']
        self.assertRaises(ValueError, argument_parser.make_option_dict, a, b)

        #more same options
        a = ['a']*10000
        b = ['a']*10000
        self.assertRaises(ValueError, argument_parser.make_option_dict, a, b)

        try:
            a = ['a', 'b', 'c']
            b = ['d', 'e', 'f']
            argument_parser.make_option_dict(a, b)
        except:
            self.fail('make_option_dict() raised an exception with a correct input')

    def test_check_option_dict_validity(self):
        #key is not str
        d = {1: 'option_argument'}
        self.assertRaises(TypeError, argument_parser.check_option_dict_validity, d)

        #option is not a single character
        d = {'aa': 'no_option_argument'}
        self.assertRaises(ValueError, argument_parser.check_option_dict_validity, d)

        #option is not an alphanumeric character
        d = {'<': 'option_argument'}
        self.assertRaises(ValueError, argument_parser.check_option_dict_validity, d)

        #key is not in ['option_argument', 'no_option_argument']
        d = {'a': 'b'}
        self.assertRaises(Exception, argument_parser.check_option_dict_validity, d)

        #correct input
        try:
            d = {'a': 'option_argument', 'b': 'no_option_argument', '2': 'option_argument'}
            argument_parser.check_option_dict_validity(d)
        except:
            self.fail('check_option_dict_validity() raised an exception with a correct input')



    def test_check_command_line_argument_validity(self):
        #argv is not a list
        self.assertFalse(argument_parser.check_command_line_argument_validity('string'))

        #argv is not a list of string
        self.assertFalse(argument_parser.check_command_line_argument_validity(['a', 2]))

        #argv is an empty list
        self.assertFalse(argument_parser.check_command_line_argument_validity([]))

        #argv has non-empty non-first elements
        self.assertFalse(argument_parser.check_command_line_argument_validity(['a', '', 'c']))

        #correctly formatted string
        self.assertTrue(argument_parser.check_command_line_argument_validity(['-A', '-1', 'a', '--']))
        
    def test_parse_command_line_arguments(self):
        #TODO implement
        pass

        

if __name__ == '__main__':
    unittest.main()
