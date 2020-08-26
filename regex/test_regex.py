#!/usr/bin/env python
import unittest
import regex
import string
import copy


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

class TestNFANode(unittest.TestCase):
    def test___repr__(self):
        a = regex.NFANode({'a': {1, 2, 3}})
        b = "{'a': {1, 2, 3}}"
        self.assertEqual(repr(a), b)

    def test___eq__(self):
        a = regex.NFANode()
        self.assertTrue(a == a)

        a = regex.NFANode({'a': {1, 1, 2, 3}})
        b = regex.NFANode({'a': {1, 2, 3}})
        self.assertTrue(a == b)

        a = regex.NFANode({'a': {1, 2, 4}})
        b = regex.NFANode({'a': {1, 2, 3}})
        self.assertFalse(a == b)

    def test___copy__(self):
        a = regex.NFANode({'a': {1, 2, 3}})
        b = copy.copy(a)
        self.assertIsNot(a, b)
        self.assertEqual(a, b)

    def test_add_transition(self):
        a = regex.NFANode()
        a.add_transition(1, 'a')
        a.add_transition(2, 'a')
        a.add_transition(3, 'b')
        a.add_transition(4, 'b')
        b = regex.NFANode({'a': {1, 2}, 'b': {3, 4}})
        self.assertEqual(a, b)

        a = regex.NFANode()
        a.add_transition(1, 'a')
        a.add_transition(1, 'a')
        a.add_transition(2, 'b')
        a.add_transition(2, 'b')
        a.add_transition(1, '')
        b = regex.NFANode({'': {1}, 'a': {1}, 'b': {2}})
        self.assertEqual(a, b)

    def test_transitions_with_symbol(self):
        n1 = regex.NFANode({'a': {1, 2, 3}, 'b': set()})

        a = n1.transitions_with_symbol('a')
        b = [1, 2, 3]
        self.assertEqual(a, b)

        a = n1.transitions_with_symbol('b')
        b = []
        self.assertEqual(a, b)

        a = n1.transitions_with_symbol('')
        b = []
        self.assertEqual(a, b)

class TestNFAPlan(unittest.TestCase):
    def test___init__(self):
        a = regex.NFAPlan(2, 0, [1], [(0, 1, 'a'), (0, 1, 'b')])
        self.assertEqual(a.n_nodes, 2)
        self.assertEqual(a.start_node, 0)
        self.assertEqual(a.accepted_nodes, [1])
        self.assertEqual(a.transitions, [(0, 1, 'a'), (0, 1, 'b')])

    def test_union_of_characters(self):
        a = regex.NFAPlan.union_of_characters([])
        b = regex.NFAPlan(2, 0, [1], [])
        self.assertEqual(a, b)

        a = regex.NFAPlan.union_of_characters(['a', 'b', ''])
        b = regex.NFAPlan(2, 0, [1], [(0, 1, 'a'), (0, 1, 'b'), (0, 1, '')])
        self.assertEqual(a, b)

    def test___repr__(self):
        a = regex.NFAPlan(4, 0, [3], [(0, 1, 'a'), (1, 2, 'b')])
        b = \
"""[n_nodes: 4,
start_node: 0,
accepted_nodes: [3],
transitions: [(0, 1, 'a'), (1, 2, 'b')]]"""

        self.assertEqual(repr(a), b)

    def test___eq__(self):
        a = regex.NFAPlan(4, 0, [3], [(0, 1, 'a'), (1, 2, 'b')])
        self.assertEqual(a, a)

        a = regex.NFAPlan(1, 0, [3], [(0, 1, 'a'), (1, 2, 'b')])
        b = regex.NFAPlan(4, 0, [3], [(0, 1, 'a'), (1, 2, 'b')])
        self.assertNotEqual(a, b)

        a = regex.NFAPlan(4, 2, [1], [(0, 1, 'a'), (1, 2, 'b')])
        b = regex.NFAPlan(4, 0, [3], [(0, 1, 'a'), (1, 2, 'b')])
        self.assertNotEqual(a, b)

        a = regex.NFAPlan(4, 2, [3], [(0, 1, 'b'), (1, 2, 'b')])
        b = regex.NFAPlan(4, 0, [3], [(0, 1, 'a'), (1, 2, 'b')])
        self.assertNotEqual(a, b)

        a = regex.NFAPlan(4, 2, [3], [(0, 1, 'b'), (1, 2, 'b')])
        b = "asdf"
        self.assertNotEqual(a, b)

        a = regex.NFAPlan(8, 2, [1, 5, 3, 2, 7], [(0, 1, 'b'), (1, 2, 'b')])
        b = regex.NFAPlan(8, 2, [1, 2, 3, 5, 7], [(1, 2, 'b'), (0, 1, 'b')])
        self.assertEqual(a, b)

    def test___copy__(self):
        a = regex.NFAPlan(4, 0, [3], [(0, 1, 'a'), (1, 2, 'b')])
        b = copy.copy(a)
        self.assertIsNot(a, b)
        self.assertEqual(a, b)

    def test_to_NFA(self):
        a = regex.NFAPlan(4, 0, [3], [(0, 1, 'a'), (1, 2, 'b')])
        a = a.to_NFA()

        n0 = regex.NFANode({'a': {1}})
        n1 = regex.NFANode({'b': {2}})
        b = regex.NFA([n0, n1, regex.NFANode(), regex.NFANode()], 0, [3])
        self.assertEqual(a, b)

        a = regex.NFAPlan(4, 0, [], [])
        a = a.to_NFA()

        b = regex.NFA([regex.NFANode(), regex.NFANode(),
                       regex.NFANode(), regex.NFANode()], 0, [])
        self.assertEqual(a, b)

    def test_apply_offset(self):
        a = regex.NFAPlan(2, 0, [2], [(0, 1, 'a'), (1, 0, 'b')])
        with self.assertRaises(ValueError):
            a.apply_offset(-123)

        a = regex.NFAPlan(2, 0, [2], [(0, 1, 'a'), (1, 0, 'b')])
        a.apply_offset(0)

        b = regex.NFAPlan(2, 0, [2], [(0, 1, 'a'), (1, 0, 'b')])
        self.assertEqual(a, b)

        a = regex.NFAPlan(2, 0, [2], [(0, 1, 'a'), (1, 0, 'b')])
        a.apply_offset(0)
        b = regex.NFAPlan(2, 0, [2], [(0, 1, 'a'), (1, 0, 'b')])
        self.assertEqual(a, b)

        a = regex.NFAPlan(2, 0, [2], [(0, 1, 'a'), (1, 0, 'b')])
        a.apply_offset(3)
        b = regex.NFAPlan(5, 3, [5], [(3, 4, 'a'), (4, 3, 'b')])
        self.assertEqual(a, b)

        a = regex.NFAPlan(10, 4, [1, 2, 3, 4], [(0, 9, 'a'), (9, 9, 'b')])
        o = 1000000
        a.apply_offset(o)
        b = regex.NFAPlan(10+o, 4+o,
                          [1+o, 2+o, 3+o, 4+o],
                          [(0+o, 9+o, 'a'), (9+o, 9+o, 'b')])
        self.assertEqual(a, b)
    def test_union(self):
        #n1:      --> 0 -a> 1 -a>(2)
        #n2:      --> 0 -b> 1 -b>(2)
        #
        #b: --> 6 -e> 0 -a> 1 -a>(2)
        #         \
        #          e> 3 -b> 4 -b>(5)

        n1 = regex.NFAPlan(3, 0, [2], [(0, 1, 'a'), (1, 2, 'a')])
        n2 = regex.NFAPlan(3, 0, [2], [(0, 1, 'b'), (1, 2, 'b')])
        a = n1.union(n2)

        b = regex.NFAPlan(7, 6, [2, 5],
                          [(0, 1, 'a'), (1, 2, 'a'), (3, 4, 'b'), (4, 5, 'b'),
                           (6, 0, ''), (6, 3, '')])

        self.assertEqual(a, b)

        #n1:      --> 0 -a> 1 -a>(2)
        #n2:      --> 0
        #
        #b: --> 4 -e> 0 -a> 1 -a>(2)
        #         \
        #          e> 3

        n1 = regex.NFAPlan(3, 0, [2], [(0, 1, 'a'), (1, 2, 'a')])
        n2 = regex.NFAPlan(1, 0, [], [])
        a = n1.union(n2)

        b = regex.NFAPlan(5, 4, [2],
                          [(4, 0, ''), (0, 1, 'a'), (1, 2, 'a'),
                           (4, 3, '')])

        self.assertEqual(a, b)

    def test_concatenate(self):
        #n1: --> 0 -a> 1 -a>(2)
        #n2: --> 0 -b> 1 -b>(2)
        #
        #b   --> 0 -a> 1 -a> 2 -e> 3 -b> 4 -b> (5)

        n1 = regex.NFAPlan(3, 0, [2], [(0, 1, 'a'), (1, 2, 'a')])
        n2 = regex.NFAPlan(3, 0, [2], [(0, 1, 'b'), (1, 2, 'b')])
        a = n1.concatenate(n2)

        b = regex.NFAPlan(6, 0, [5],
                          [(0, 1, 'a'), (1, 2, 'a'), (2, 3, ''),
                           (3, 4, 'b'), (4, 5, 'b')])
        self.assertEqual(a, b)

        #n1: --> 0 -a> 1 -a> 2
        #n2: --> 0 -b> 1 -b>(2)
        #
        #b   --> 0 -a> 1 -a> 2     3 -b> 4 -b> (5)

        n1 = regex.NFAPlan(3, 0, [], [(0, 1, 'a'), (1, 2, 'a')])
        n2 = regex.NFAPlan(3, 0, [2], [(0, 1, 'b'), (1, 2, 'b')])
        a = n1.concatenate(n2)

        b = regex.NFAPlan(6, 0, [5],
                          [(0, 1, 'a'), (1, 2, 'a'),
                           (3, 4, 'b'), (4, 5, 'b')])
        self.assertEqual(a, b)

    def test_star(self):
        #n1:     --> 0 -a> 1 -a>(2)
        #
        #b -->(3)-e> 0 -a> 1 -a>(2)
        #            ^         /
        #             \------e-

        n1 = regex.NFAPlan(3, 0, [2], [(0, 1, 'a'), (1, 2, 'a')])
        a = n1.star()

        b = regex.NFAPlan(4, 3, [2, 3],
                          [(3, 0, ''), (0, 1, 'a'), (1, 2, 'a'), (2, 0, '')])
        self.assertEqual(a, b)

        #n1:     --> 0
        #
        #b -->(1)-e> 0

        n1 = regex.NFAPlan(1, 0, [], [])
        a = n1.star()

        b = regex.NFAPlan(2, 1, [1], [(1, 0, '')])
        self.assertEqual(a, b)
    def test_plus(self):
        #n1:     --> 0 -a> 1 -a>(2)
        #
        #b --> 0 -a> 1 -a> 2 -e> (6)-e> 3 -a> 4 -a>(5)
        #                               ^         /
        #                                \------e-
        n1 = regex.NFAPlan(3, 0, [2], [(0, 1, 'a'), (1, 2, 'a')])
        a = n1.plus()

        b = regex.NFAPlan(7, 0, [6, 5],
                          [(0, 1, 'a'), (1, 2, 'a'), (2, 6, ''), (6, 3, ''),
                           (3, 4, 'a'), (4, 5, 'a'), (5, 3, '')])
        self.assertEqual(a, b)
    def test_question(self):
        #n1:   --> 0 -a> 1 -a>(2)
        #
        #b:  5 -e> 0 -a> 1 -a>(2)
        #      \
        #       e> 3 -e>(4)
        n1 = regex.NFAPlan(3, 0, [2], [(0, 1, 'a'), (1, 2, 'a')])
        a = n1.question()

        b = regex.NFAPlan(6, 5, [2, 4],
                          [(5, 0, ''), (0, 1, 'a'), (1, 2, 'a'),
                           (5, 3, ''), (3, 4, '')])


class TestNFA(unittest.TestCase):

    def test___init__(self):
        n0 = regex.NFANode({'a': {0}})
        n1 = regex.NFANode({'b': {0}})
        nodes = [n0, n1]
        accepted_nodes = [0]
        a = regex.NFA(nodes, 0, accepted_nodes)
        self.assertEqual(a.nodes, nodes)
        self.assertEqual(a.start_node, 0)
        self.assertEqual(a.accepted_nodes, accepted_nodes)
        #test copying
        self.assertIsNot(a.nodes, nodes)
        self.assertIsNot(a.nodes[0], n0)
        self.assertIsNot(a.accepted_nodes, accepted_nodes)

    def test___eq__(self):
        n0 = regex.NFANode({'a': {0}})
        n1 = regex.NFANode({'b': {0}})
        nodes = [n0, n1]
        accepted_nodes = [0]
        a = regex.NFA(nodes, 0, accepted_nodes)

        self.assertEqual(a, a)
        self.assertNotEqual(a, " ")

        n0 = regex.NFANode({'a': {0}})
        n1 = regex.NFANode({'b': {0}})
        n2 = regex.NFANode({'a': {1}})
        a = regex.NFA([n0, n1], 0, [0])
        b = regex.NFA([n2, n1], 0, [0])
        self.assertNotEqual(a, b)

        n0 = regex.NFANode({'a': {0}})
        n1 = regex.NFANode({'b': {0}})
        a = regex.NFA([n0, n1], 0, [0])
        b = regex.NFA([n0, n1], 1, [0])
        self.assertNotEqual(a, b)

        n0 = regex.NFANode({'a': {0}})
        n1 = regex.NFANode({'b': {0}})
        a = regex.NFA([n0, n1], 0, [0])
        b = regex.NFA([n0, n1], 0, [1])
        self.assertNotEqual(a, b)

    def test___repr__(self):
        n0 = regex.NFANode({'a': {0}})
        n1 = regex.NFANode({'b': {0}})
        a = str(regex.NFA([n0, n1], 0, [0]))
        b = \
"""[nodes: [{'a': {0}}, {'b': {0}}],
start_node: 0,
accepted_nodes: [0]]"""
        self.assertEqual(a, b)

    def test_reachable_with_symbol(self):
        #n1: --> 0 -a> 1 -a> 2
        n1 = regex.NFAPlan(3, 0, [], [(0, 1, 'a'), (1, 2, 'a')]).to_NFA()
        a = n1.reachable_with_symbol([0], 'a')
        self.assertEqual(a, [1])

        #n1: --> 0 -a> 1 -a> 2
        n1 = regex.NFAPlan(3, 0, [], [(0, 1, 'a'), (1, 2, 'a')]).to_NFA()
        a = n1.reachable_with_symbol([0], 'b')
        self.assertEqual(a, [])

        #n1: --> 0 -a> 1 -a> 2
        n1 = regex.NFAPlan(3, 0, [], [(0, 1, 'a'), (1, 2, 'a')]).to_NFA()
        a = n1.reachable_with_symbol([0, 1], 'a')
        self.assertEqual(a, [1, 2])

    def test_reachable_with_empty(self):
        #n1: --> 0 -a> 1 -a> 2
        n1 = regex.NFAPlan(3, 0, [], [(0, 1, 'a'), (1, 2, 'a')]).to_NFA()
        a = n1.reachable_with_empty([0])
        self.assertEqual(a, [0])

        #b -->(3)-e> 0 -a> 1 -a>(2)
        #            ^         /
        #             \------e-
        n1 = regex.NFAPlan(4, 3, [2, 3],
                          [(3, 0, ''), (0, 1, 'a'), (1, 2, 'a'), (2, 0, '')])
        n1 = n1.to_NFA()
        a = n1.reachable_with_empty([3])
        self.assertEqual(a, [3, 0])

    def test_evaluate(self):
        #n1: --> 0 -a> 1 -a>(2)
        n1 = regex.NFAPlan(3, 0, [2], [(0, 1, 'a'), (1, 2, 'a')]).to_NFA()
        a = n1.evaluate("aa")
        self.assertTrue(a)

        #n1: --> 0 -a> 1 -a>(2)
        n1 = regex.NFAPlan(3, 0, [2], [(0, 1, 'a'), (1, 2, 'a')]).to_NFA()
        a = n1.evaluate("aa ")
        self.assertFalse(a)

        #n1: --> 0 -a> 1 -a>(2)
        n1 = regex.NFAPlan(3, 0, [2], [(0, 1, 'a'), (1, 2, 'a')]).to_NFA()
        a = n1.evaluate("a")
        self.assertFalse(a)

        #n1 -->(3)-e> 0 -a> 1 -a>(2)
        #            ^         /
        #             \------e-
        n1 = regex.NFAPlan(4, 3, [2, 3],
                          [(3, 0, ''), (0, 1, 'a'), (1, 2, 'a'), (2, 0, '')])
        n1 = n1.to_NFA()
        for i in range(20):
            if i % 2 == 0:
                a = n1.evaluate("")
                self.assertTrue(a)
            else:
                a = n1.evaluate("a")
                self.assertFalse(a)

        #b --> 0 -e> 1 -e> 2 -e>(3)
        n1 = regex.NFAPlan(4, 0, [3], [(0, 1, ''), (1, 2, ''), (2, 3, '')])
        n1 = n1.to_NFA()
        a = n1.evaluate('')
        self.assertTrue(a)

        a = n1.evaluate('a')
        self.assertFalse(a)

if __name__ == '__main__':
    unittest.main()
