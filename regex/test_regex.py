#!/usr/bin/env python
import unittest
import regex


class TestParseTreeNode(unittest.TestCase):
    def test_equal(self):
        a = regex.ParseTreeNode(meta='.')
        b = regex.ParseTreeNode(meta='.')
        self.assertTrue(a == b)

        a = regex.ParseTreeNode(meta='.')
        b = regex.ParseTreeNode(meta='|')
        self.assertTrue(a != b)

        a = regex.ParseTreeNode(normal='a')
        b = regex.ParseTreeNode(normal='a')
        self.assertTrue(a == b)

        a = regex.ParseTreeNode(normal='a')
        b = regex.ParseTreeNode(normal='b')
        self.assertTrue(a != b)

        a = regex.ParseTreeNode(normal='a')
        b = regex.ParseTreeNode(meta='a')
        self.assertTrue(a != b)

        a = regex.ParseTreeNode(normal='a')
        b = regex.ParseTreeNode(operation='|')
        self.assertTrue(a != b)

        a = regex.ParseTreeNode(operation='concatenation')
        b = regex.ParseTreeNode(operation='|')
        self.assertTrue(a != b)

        c1 = regex.ParseTreeNode(normal='a')
        c2 = regex.ParseTreeNode(normal='b')
        a = regex.ParseTreeNode(children=[c1], operation='*')
        b = regex.ParseTreeNode(children=[c2], operation='*')
        self.assertTrue(a != b)

        c1=regex.ParseTreeNode(normal='a')
        c2=regex.ParseTreeNode(normal='a')
        a = regex.ParseTreeNode(children=[c1], operation='*')
        b = regex.ParseTreeNode(children=[c2], operation='*')
        self.assertTrue(a == b)

        c1 = regex.ParseTreeNode(normal='a')
        c2 = regex.ParseTreeNode(normal='a')
        a = regex.ParseTreeNode(normal='a')
        b = regex.ParseTreeNode(normal='b')
        self.assertTrue(a != b)

    def test___str__(self):
        a = regex.ParseTreeNode(normal='a')
        a = str(a)
        self.assertEqual(a, "NNa")

        a = regex.ParseTreeNode(normal='')
        a = str(a)
        self.assertEqual(a, "NN_")

        a = regex.ParseTreeNode(meta='|')
        a = str(a)
        self.assertEqual(a, "N|N")

        a = regex.ParseTreeNode(operation='|')
        a = str(a)
        self.assertEqual(a, "|NN")

        a = regex.ParseTreeNode(operation='concatenation')
        a = str(a)
        self.assertEqual(a, "cNN")

        c1 = regex.ParseTreeNode(normal='a')
        a = regex.ParseTreeNode(children=[c1], operation='*')
        a = str(a)
        self.assertEqual(a, "*NN---NNa")

        c1 = regex.ParseTreeNode(normal='a')
        a = regex.ParseTreeNode(children=[c1, c1], operation='|')
        a = str(a)
        b = \
"""
|NN---NNa
|
+-----NNa"""[1:]


        c1 = regex.ParseTreeNode(normal='a')
        a = regex.ParseTreeNode(children=[c1, c1, c1], operation='c')
        a = str(a)
        b = \
"""
cNN---NNa
|
+-----NNa
|
+-----NNa"""[1:]
        self.assertEqual(a, b)

        c1 = regex.ParseTreeNode(normal='1')
        c2 = regex.ParseTreeNode(normal='2')
        c3 = regex.ParseTreeNode(normal='3')
        c4 = regex.ParseTreeNode(normal='4')
        p1 = regex.ParseTreeNode(children=[c1, c2], operation='c')
        p2 = regex.ParseTreeNode(children=[c3, c4], operation='|')
        p3 = regex.ParseTreeNode(children=[p1, p2], operation='c')
        a = str(p3)
        b = \
"""
cNN---cNN---NN1
|     |
|     +-----NN2
|
+-----|NN---NN3
      |
      +-----NN4"""[1:]

        self.assertEqual(a, b)

class TestRegexParsing(unittest.TestCase):
    def test_process_union(self):
        a = regex.process_union([regex.ParseTreeNode(normal='a')])
        b = [regex.ParseTreeNode(normal='a')]
        self.assertTrue(a == b)

        a = regex.process_union([regex.ParseTreeNode(normal='b')])
        b = [regex.ParseTreeNode(normal='a')]
        self.assertTrue(a != b)

        tmp = [regex.ParseTreeNode(normal='a'),
               regex.ParseTreeNode(meta='|'),
               regex.ParseTreeNode(normal='b')]
        a = regex.process_union(tmp)
        c1 = regex.ParseTreeNode(normal='a')
        c2 = regex.ParseTreeNode(normal='b')
        b = regex.ParseTreeNode(children=[c1, c2], operation='|')
        b = [b]
        self.assertEqual(a, b)

        n1 = regex.ParseTreeNode(normal='a')
        n2 = regex.ParseTreeNode(children=[n1], operation='*')
        tmp = [n2,
               regex.ParseTreeNode(meta='|'),
               regex.ParseTreeNode(normal='b')]
        a = regex.process_union(tmp)
        n1 = regex.ParseTreeNode(normal='a')
        n2 = regex.ParseTreeNode(children=[n1], operation='*')
        n3 = regex.ParseTreeNode(normal='b')
        b = regex.ParseTreeNode(children=[n2, n3], operation='|')
        b = [b]
        self.assertEqual(a, b)


        tmp = [regex.ParseTreeNode(meta='|')]
        a = regex.process_union(tmp)
        n1 = regex.ParseTreeNode(normal='')
        n2 = regex.ParseTreeNode(normal='')
        b = regex.ParseTreeNode(children=[n1, n2], operation='|')
        b = [b]
        self.assertEqual(a, b)

        tmp = [regex.ParseTreeNode(meta='.'),
               regex.ParseTreeNode(meta='|'),
               regex.ParseTreeNode(meta='.')]
        a = regex.process_union(tmp)
        n1 = regex.ParseTreeNode(meta='.')
        n2 = regex.ParseTreeNode(meta='.')
        b = regex.ParseTreeNode(children=[n1, n2], operation='|')
        b = [b]
        self.assertEqual(a, b)

        tmp = [regex.ParseTreeNode(meta='|'),
               regex.ParseTreeNode(meta='|')]
        a = regex.process_union(tmp)
        n1 = regex.ParseTreeNode(normal='')
        n2 = regex.ParseTreeNode(normal='')
        n3 = regex.ParseTreeNode(children=[n1, n2], operation='|')
        n4 = regex.ParseTreeNode(normal='')
        b = regex.ParseTreeNode(children=[n3, n4], operation='|')
        b = [b]
        self.assertEqual(a, b)

        tmp = [regex.ParseTreeNode(meta='('),
               regex.ParseTreeNode(meta='|')]

        with self.assertRaises(Exception):
            regex.parse_union(tmp)

        tmp = [regex.ParseTreeNode(meta='|'),
               regex.ParseTreeNode(meta=')')]

        with self.assertRaises(Exception):
            regex.parse_union(tmp)

    def test_process_concatenation(self):
        a = regex.process_concatenation([regex.ParseTreeNode(normal='a')])
        b = [regex.ParseTreeNode(normal='a')]
        self.assertEqual(a, b)

        tmp = [regex.ParseTreeNode(normal='a'),
               regex.ParseTreeNode(normal='a')]
        a = regex.process_concatenation(tmp)
        c1 = regex.ParseTreeNode(normal='a')
        c2 = regex.ParseTreeNode(normal='a')
        b = regex.ParseTreeNode(children=[c1, c2], operation='concatenation')
        b = [b]
        self.assertEqual(a, b)

        tmp = [regex.ParseTreeNode(normal='a'),
               regex.ParseTreeNode(normal='b'),
               regex.ParseTreeNode(normal='c')]
        a = regex.process_concatenation(tmp)
        n1 = regex.ParseTreeNode(normal='a')
        n2 = regex.ParseTreeNode(normal='b')
        n3 = regex.ParseTreeNode(normal='c')
        n4 = regex.ParseTreeNode(children=[n1, n2], operation='concatenation')
        b = regex.ParseTreeNode(children=[n4, n3], operation='concatenation')
        b = [b]
        self.assertEqual(a, b)

        tmp = [regex.ParseTreeNode(normal='a'),
               regex.ParseTreeNode(normal='b'),
               regex.ParseTreeNode(meta='|'),
               regex.ParseTreeNode(normal='c'),
               regex.ParseTreeNode(normal='d')]
        a = regex.process_concatenation(tmp)
        n1 = regex.ParseTreeNode(normal='a')
        n2 = regex.ParseTreeNode(normal='b')
        n3 = regex.ParseTreeNode(children=[n1, n2], operation='concatenation')
        n4 = regex.ParseTreeNode(normal='c')
        n5 = regex.ParseTreeNode(normal='d')
        n6 = regex.ParseTreeNode(children=[n4, n5], operation='concatenation')
        n7 = regex.ParseTreeNode(meta='|')
        b = [n3, n7, n6]
        self.assertEqual(a, b)

    def test_process_unary(self):
        a = regex.process_unary([regex.ParseTreeNode(normal='a')])
        b = [regex.ParseTreeNode(normal='a')]
        self.assertEqual(a, b)

        tmp = [regex.ParseTreeNode(normal='a'),
               regex.ParseTreeNode(meta='*')]
        a = regex.process_unary(tmp)
        c1 = regex.ParseTreeNode(normal='a')
        b = regex.ParseTreeNode(children=[c1], operation='*')
        b = [b]
        self.assertEqual(a, b)

        tmp = [regex.ParseTreeNode(meta='*'),
               regex.ParseTreeNode(normal='a')]
        with self.assertRaises(ValueError):
            regex.process_unary(tmp)

        tmp = [regex.ParseTreeNode(meta='|'),
               regex.ParseTreeNode(meta='*')]
        with self.assertRaises(ValueError):
            regex.process_unary(tmp)

        tmp = [regex.ParseTreeNode(normal='a'),
               regex.ParseTreeNode(meta='+'),
               regex.ParseTreeNode(normal='b'),
               regex.ParseTreeNode(meta='?'),
               regex.ParseTreeNode(meta='|'),
               regex.ParseTreeNode(normal='c'),
               regex.ParseTreeNode(meta='*')]
        a = regex.process_unary(tmp)
        n1 = regex.ParseTreeNode(normal='a')
        n2 = regex.ParseTreeNode(children=[n1], operation='+')
        n3 = regex.ParseTreeNode(normal='b')
        n4 = regex.ParseTreeNode(children=[n3], operation='?')
        n5 = regex.ParseTreeNode(meta='|')
        n6 = regex.ParseTreeNode(normal='c')
        n7 = regex.ParseTreeNode(children=[n6], operation='*')
        b = [n2, n4, n5, n7]
        self.assertEqual(a, b)
    def test_parse_wo_parentheses(self):
        tmp = [regex.ParseTreeNode(normal='a'),
               regex.ParseTreeNode(meta='+'),
               regex.ParseTreeNode(normal='b'),
               regex.ParseTreeNode(normal='c'),
               regex.ParseTreeNode(meta='?'),
               regex.ParseTreeNode(meta='|'),
               regex.ParseTreeNode(normal='d'),
               regex.ParseTreeNode(meta='*')]
        a = regex.parse_wo_parentheses(tmp)

        n1 = regex.ParseTreeNode(normal='a')
        n2 = regex.ParseTreeNode(children=[n1], operation='+')
        n3 = regex.ParseTreeNode(normal='b')
        n4 = regex.ParseTreeNode(children=[n2, n3], operation='concatenation')

        n5 = regex.ParseTreeNode(normal='c')
        n6 = regex.ParseTreeNode(children=[n5], operation='?')

        n7 = regex.ParseTreeNode(children=[n4, n6], operation='concatenation')

        n8 = regex.ParseTreeNode(normal='d')
        n9 = regex.ParseTreeNode(children=[n8], operation='*')

        b = regex.ParseTreeNode(children=[n7, n9], operation='|')
        self.assertEqual(a, b)

        a = regex.parse_wo_parentheses([])
        self.assertIsNone(a)

    def test_parse_nodes_to_tree(self):
        tmp = [regex.ParseTreeNode(meta='(')]
        with self.assertRaises(ValueError):
            regex.parse_nodes_to_tree(tmp)
        tmp = [regex.ParseTreeNode(meta='('),
               regex.ParseTreeNode(meta=')'),
               regex.ParseTreeNode(meta=')')]
        with self.assertRaises(ValueError):
            regex.parse_nodes_to_tree(tmp)

        a = regex.parse_nodes_to_tree([])
        self.assertIsNone(a)

        tmp = [regex.ParseTreeNode(normal='a'),
               regex.ParseTreeNode(meta=  '('),
               regex.ParseTreeNode(normal='b'),
               regex.ParseTreeNode(meta=  '|'),
               regex.ParseTreeNode(normal='c'),
               regex.ParseTreeNode(meta=  ')'),
               regex.ParseTreeNode(meta=  '?')]
        a = regex.parse_nodes_to_tree(tmp)

        n1 = regex.ParseTreeNode(normal='a')

        n2 = regex.ParseTreeNode(normal='b')
        n3 = regex.ParseTreeNode(normal='c')
        n4 = regex.ParseTreeNode(children=[n2, n3], operation='|')
        n5 = regex.ParseTreeNode(children=[n4], operation='?')

        b = regex.ParseTreeNode(children=[n1, n5], operation='concatenation')
        self.assertEqual(a, b)



        tmp = [regex.ParseTreeNode(meta=  '('),
               regex.ParseTreeNode(meta=  ')'),
               regex.ParseTreeNode(meta=  '('),
               regex.ParseTreeNode(meta=  '('),
               regex.ParseTreeNode(meta=  '('),
               regex.ParseTreeNode(normal='a'),
               regex.ParseTreeNode(meta=  ')'),
               regex.ParseTreeNode(meta=  ')'),
               regex.ParseTreeNode(meta=  ')'),
               regex.ParseTreeNode(meta=  '('),
               regex.ParseTreeNode(meta=  '('),
               regex.ParseTreeNode(meta=  '('),
               regex.ParseTreeNode(meta=  '('),
               regex.ParseTreeNode(normal='b'),
               regex.ParseTreeNode(meta=  '|'),
               regex.ParseTreeNode(normal='c'),
               regex.ParseTreeNode(meta=  ')'),
               regex.ParseTreeNode(meta=  ')'),
               regex.ParseTreeNode(meta=  ')'),
               regex.ParseTreeNode(meta=  ')'),
               regex.ParseTreeNode(meta=  '?')]
        a = regex.parse_nodes_to_tree(tmp)

        n1 = regex.ParseTreeNode(normal='a')

        n2 = regex.ParseTreeNode(normal='b')
        n3 = regex.ParseTreeNode(normal='c')
        n4 = regex.ParseTreeNode(children=[n2, n3], operation='|')
        n5 = regex.ParseTreeNode(children=[n4], operation='?')

        b = regex.ParseTreeNode(children=[n1, n5], operation='concatenation')
        self.assertEqual(a, b)


        tmp = [regex.ParseTreeNode(meta=  '('),
               regex.ParseTreeNode(meta=  '*'),
               regex.ParseTreeNode(meta=  ')')]
        with self.assertRaises(ValueError):
            regex.parse_nodes_to_tree(tmp)

        tmp = [regex.ParseTreeNode(meta=  '('),
               regex.ParseTreeNode(meta=  '|'),
               regex.ParseTreeNode(meta=  ')')]
        a = regex.parse_nodes_to_tree(tmp)

        n1 = regex.ParseTreeNode(normal='')
        n2 = regex.ParseTreeNode(normal='')
        b = regex.ParseTreeNode(children=[n1, n2], operation='|')
        self.assertEqual(a, b)

    def test_regex_to_parse_tree_nodes(self):
        a = regex.regex_to_parse_tree_nodes('')
        self.assertEqual(a, [])

        a = regex.regex_to_parse_tree_nodes('a')
        b = [regex.ParseTreeNode(normal='a')]
        self.assertEqual(a, b)

        a = regex.regex_to_parse_tree_nodes(r'\?')
        b = [regex.ParseTreeNode(normal='?')]
        self.assertEqual(a, b)

        a = regex.regex_to_parse_tree_nodes(r'\a')
        b = [regex.ParseTreeNode(normal='a')]
        self.assertEqual(a, b)

        a = regex.regex_to_parse_tree_nodes(r'\|')
        b = [regex.ParseTreeNode(normal='|')]
        self.assertEqual(a, b)

        a = regex.regex_to_parse_tree_nodes(r'*')
        b = [regex.ParseTreeNode(meta='*')]
        self.assertEqual(a, b)

        a = regex.regex_to_parse_tree_nodes(r'*')
        b = [regex.ParseTreeNode(meta='*')]
        self.assertEqual(a, b)

        a = regex.regex_to_parse_tree_nodes(r'a*|\?b')
        b = [regex.ParseTreeNode(normal='a'),
             regex.ParseTreeNode(meta=  '*'),
             regex.ParseTreeNode(meta=  '|'),
             regex.ParseTreeNode(normal='?'),
             regex.ParseTreeNode(normal='b')]
        self.assertEqual(a, b)

    def test_parse_regex(self):
        a = regex.parse_regex("")
        self.assertIsNone(a)

        a = regex.parse_regex(" ")
        b = regex.ParseTreeNode(normal=' ')
        self.assertEqual(a, b)

        a = regex.parse_regex("abc")
        n1 = regex.ParseTreeNode(normal='a')
        n2 = regex.ParseTreeNode(normal='b')
        n3 = regex.ParseTreeNode(children=[n1, n2], operation='concatenation')
        n4 = regex.ParseTreeNode(normal='c')
        b = regex.ParseTreeNode(children=[n3, n4], operation='concatenation')
        self.assertEqual(a, b)

        a = regex.parse_regex("()(((())))\|(b|)c?")
        n1 = regex.ParseTreeNode(normal='|')
        n2 = regex.ParseTreeNode(normal='b')
        n3 = regex.ParseTreeNode(normal='')

        n4 = regex.ParseTreeNode(children=[n2, n3], operation='|')
        n5 = regex.ParseTreeNode(children=[n1, n4], operation='concatenation')

        n6 = regex.ParseTreeNode(normal='c')
        n7 = regex.ParseTreeNode(children=[n6], operation='?')

        b = regex.ParseTreeNode(children=[n5, n7], operation='concatenation')
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
