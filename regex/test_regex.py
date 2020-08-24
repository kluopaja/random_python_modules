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

if __name__ == '__main__':
    unittest.main()
