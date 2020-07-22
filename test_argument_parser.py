#!/usr/bin/env python
import unittest
import argument_parser

class TestArgumentParser(unittest.TestCase):
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

        

if __name__ == '__main__':
    unittest.main()
