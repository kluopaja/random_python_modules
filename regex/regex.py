#!/usr/bin/env python

"""

Background
----------
For more deep treatment of the topic the reader should read the Sipser book.

One problem in computing is how to define a sets of strings. For 
example, how could one detect if a string s is a correctly formatted person's
name or username.

One way to do this would be to write a computer program (here means using a
turing machine) that returns 1 if the string belongs to desired set or 0 if it
doesn't. Such a program might consist of statements like:
if s[0].isupper(): ...

However, this might get somewhat complicated from both the theoretical and
practical point of view. 

Finite languages
----------------
One simple way to define sets of strings is to use a finite automaton. For this
we need some definitions:

    Alphabet is a finite set of symbols.

    String is a finite sequence of symbols where every symbol belongs to a
    certain alphabet.

    A set of strings is called a language.

    A concatenation of strings a and b is marked by ab and means joining
    strings a and b:
        let a='abc' and b='def', then ab = 'abcdef'

A finite automaton is a simple computational model which takes a string
as an input and then either accepts or rejects it. The set of strings,
that is a language, recognized by a finite automaton A is marked by L(A)

The set of languages defined by finite automata are called finite languages.

The finite automaton is defined by 5 parameters:
    1. The set of automaton states, here denoted by Q
    2. An alphabet, here denoted by S
    3. A transition function, here denoted by d
    4. A start state, which is an element of Q, here denoted by q_0
    5. A subset of Q, the accepted states, here denoted by F

The transition function d is a function from a set (Q X E) to the set Q. That
is, the function takes two parameters X and Y where X is an automaton state
and Y is a symbol of the alphabet S.

The automaton works by starting from the start state q_0, reading the input 
string T one symbol at a time and changing the automaton state based on the
read symbol and current state as defined by the transition function d. If, 
after processing the whole string, the automaton is in one of the accepted 
states, then the automaton accepts the string. Otherwise the automaton rejects
the string.

In other words:
    Let the current state of the automaton be C.
    def test_string(T):
        C = q_0
        for i in range(len(T)):
            C = d(C, T[i])

        if C in F:
            return "Accept"
        else:
            return "Reject"

It might be helpful to think the finite automata as a graph and function
d as labeled directed edges.

It is therefore quite easy to evaluate the string once the finite automaton
has been constructed. The question that remains is how to construct one.

It is easy to construct very simple finite automata such as those recognizing:
    1. A certain symbol of the alphabet S
    2. An empty string, {_}
    3. Nothing at all, {} (empty set)

Fortunately, also more complicated automata can be constructed from these
simple automata using the following operations
    1. Union
        If we have two finite automata A and B recognizing languages L(A) and
        L(B), we know how to construct a finite automaton C such that 
        L(C) = L(A) U L(B). That is, finite automaton C recognizes strings by
        at least A or B.

    2. Concatenation
        If we have two finite automata A and B recognizing L(A) and L(B), 
        we know how to construct a finite automaton C such that if w \in L(A)
        and v \in L(B), then wv \in L(C), where wv is the concatenation of w 
        and v. We mark this by L(C) = L(A)L(B)

    3. Kleene star
        If a finite automaton A recognizes L(A), then we know how to construct
        a finite automaton B such that 
        L(B) = L(A)* = {_} U L(A) U L(A)L(A) U L(A)L(A)L(A) U ...

        Where {_} is the language recognizing an empty string. 

        In other words, L(A)* is the language formed by concatenating
        the strings of language L(A) arbitrarily (also 0 or 1) times with
        itselves.

    4. Intersection
        If we have two finite automata A and B recognizing L(A) and L(B),
        we know how to  construct a finite automaton C such that
        L(C) = L(A) \cap L(B).  That is, automaton C recognizes string that are
        recognized by both A and B.

    5. Negation
        If a finite automaton A recognizes L(A), then we know how to construct
        a finite automaton C such that L(C) = L(A)^C where ^C marks the
        complement of a set. That is, automaton C recognizes exactly those
        strings that automaton A doesn't recognize. 


It can be shown that for every finite language A, a finite automaton 
B, such that L(B) = A, can be constructed using only the previous operations
1-3.

We might then imagine using the knowledge to construct finite automata to solve
our problem of matching a string in a computer program. Perhaps our code would
looks something like following:
    def check_string(s):
        #Initialize the base cases
        S1 = FiniteAutomaton('A')
        S2 = FiniteAutomaton('B')

        #Construct automaton
        A1 = union(S1, S2)
        A2 = concatenate(S1, S2)
        A3 = concatenate(A1, A2)
        A4 = star(A3)

        return A4.match(s)


We would clearly benefit from having concise notation that is human readable
and standardized. This leads us to regular expressions.

Regular expression
------------------

Regular expressions are a way to describe regular languages. It should be noted
that some regular expression implementations also allow some additional
operations so that the result is no more a regular language. We will not
consider such operations here.


Definition:
    Regular expressions corresponding to the simple languages
        1. a is a regular expression if a belongs to the selected alphabet.
            L(a) = {a}
        2. @ is a regular expression such that L(@) = {} (an empty set)
        3. _ is a regular expression such that L(_) = {_} (an empty string)

    Other regular expressions can be formed by applying the following
    operations:
        1. Union
            Let R_1 and R_2 be regular expression. Then also (R_1|R_2)
            is a regular expression and L((R_1|R_2)) = L(R_1) U L(R_2)
        2. Concatenation
            Let R_1 and R_2 be regular expression. Then also (R_1R_2)
            is a regular expression and L((R_1R_2)) = L(R_1)L(R_2)
        3. Kleene star
            Let R be a regular expression, then also (R*) is a regular
            expression and L((R*)) = L(R)*

What if there were two sequences of operations leading to a regular
expression R but two different languages? This would not be desirable as we
want to define a language with a regular expression. We note that 
this is clearly not the case for every regular expression consisting of only
one character. By noting that every regular expression is either one letter
or enclosed in parentheses we can also see that if we have a more complex
regular expression R, then there is always only one operation which could
have formed R. Moreover, for every operation there is only a one way to
select regular expressions R1 (and R2) to form R. Thus only one way to 
define the language L(R).

#pllk mitä mieltä tuosta^?

We note that if we have the instructions to construct some finite automaton
based on the rules of the previous section, we can simply apply the same 
sequence of operations to constuct a regular expessions describing the same 
language.

The next challenge is to do the opposite i.e. to find out the way to decompose
a regular expression to the operations used to form it. This is done by forming
a parse tree of the expression. Every node of the parse tree corresponds to
some regular expression. The leaves are always one of our three simple
languages. 

Lets then consider an internal node r. Node r corresponds to a regular
expression formed from its child(ren) by applying some of our 3 operations.
This operation is also stored at the node r.

The root of the parse tree is the whole regular expression.

Parsing regular expressions in the most basic form is easy and can be basically
done by constructing the tree formed by the parentheses.

Unfortunately for us but fortunately for the user parsing the regular
expression is complicated by a few addional details:
        We include the following shorthand notations:
            (R(R*)) = (R+)
            (R|_) = (R?)
            . = (a|(b|c(... where a,b,c are the characters of the alphabet

        Also empty string can be denoted simply by ''
            (_|a) = (|a)

        The different operators are evaluated in the order: */+/?,
        concatenation, union.

        Operators are evaluated from left to right.

        All excessive parentheses can simply be left out.

        For example:
            (a(b(a(b(a))))) = ababa
            (a|((b*)c)) = a|b*c

NOTE: Should I comment something that regular expressions are still well
defined? How to prove this? pllk!!!

To parse these we first form a tree just based on the parentheses.
To be continued...

"""


class NFA:
    """Implements non-deterministic finite automaton


    """
    def __init__(self, states, transition_dict, start_state, accepted_states):
        self.states = states
        self.transition_dict = transition_dict
        self.start_state = start_state
        self.accepted_states = accepted_states

    def evaluate(self, s):
        """Determines if the NFA accepts string s
        """
        pass
    def union(self, other):
        """self = self U other

        """
        pass

    def concatenate(self, other):
        """self = Concatenate(self, other)

        """
        pass

    def star(self):
        """self = self*
        """
        pass

    def plus(self):
        """self = self+
        """
        pass

    def question(self):
        """self = self?
        """
        pass


class ParseTreeNode:
    def __init__(self):
        self.children = []
        #meta and normal are used for leaves
        self.meta = ''
        self.normal = ''

        #operation is used for internal nodes
        self.operation = ''

    def add_child(self):
        pass


def parse_regex(regex):
    """Generates parse tree from regex

    Parameters
    ----------
    regex : str


    Returns
    -------
    root : ParseTreeNode
        Root of the generated parse tree corresponding to regex


    Notes
    -----
    The parsing is done by representing the regex as a list and then replacing
    object (initially all leaf nodes) with parse tree nodes and placing the
    previous nodes as children of this new node

    This function converts the regex (str) to a list of ParseTreeNodes

    Escaped characters are represend as strings of two characters e.g. \)
    """

    i = 0
    regex_object_list = []
    while i < len(regex):
        new_node = ParseTreeNode()
        if regex[i] == '\\':
            new_node.normal = regex[i+1:i+2]
            i += 2
        else:
            if regex[i] in '*+?|()':
                new_node.meta = regex[i]
            else:
                new_node.normal = regex[i]
            i += 1

        regex_object_list.append(new_node)

    root = parse_regex_list(list(regex))
    return root


#TODO rename the regex_object_list
def parse_regex_list(regex_object_list):
    """Generates parse tree from regex object list

    Parameters
    ----------
    regex_object_list : list of ParseTreeNodes

    Returns
    -------
    root : ParseTreeNode
        Root of the generated parse tree corresponding to regex_object_list

    """
    
    #regex object lists without any parentheses
    #regex_lists[i] corresponds to a list which is enclosed in i parentheses
    regex_lists = [[]]

    for i in range(len(regex_object_list)):
        if regex_object_list[i].meta == '(':
            regex_lists.append([])
            open_parentheses += 1

        elif regex_object_list[i].meta == ')':
            if len(regex_list) <= 1:
                raise ValueError("Incorrect parentheses in regex_object_list")

            tmp = parse_wo_parentheses(regex_lists[-1])
            regex_lists[-2].append(tmp)
            regex_lists.pop()
        else:
            regex_lists[-1].append(regex_object_list[i])

    root = parse_wo_parentheses(regex_lists[0])

def parse_wo_parentheses(regex_object_list):
    """Parses a regex object list not containing any parentheses

    Parameters
    ----------
    regex_object_list : list of characters or ParseTreeNodes
        Should not contain any parentheses

    Returns
    -------
    root : ParseTreeNode
        Root of the generated parse tree corresponding to regex_object_list
    
    """

    result1 = []
    #*/+/?
    for i in range(len(regex_object_list)):
        if regex_object_list[i].meta in ['*', '+', '?']:
            if len(result1) == 0:
                raise ValueError("regex_object_list starts with */+/?")

            new_node = ParseTreeNode(children=[result1[-1]], 
                                     operation=regex_object_list[i].meta)

            result1[-1] = new_node
        else:
            result1.append(regex_object_list[i])

    result2 = []

    #concatenation
    for i in range(len(result1)):
        result2.append(result1[i])
        if len(result2 >= 2):
            if result2[-2].meta == '' and result2[-1].meta == '':
                new_node = ParseTreeNode(children=result2[-2],
                                         operation='concatenation')
                result2[-2:] = []
                reuslt2.append(new_node)

    #union

    i = 0
    result3 = []
    while i < len(result2):
        if result2[i].meta == '|':
            #in some cases we need to create empty nodes here
            
            #['|', ...]
            if i == 0:
                left_child = ParseTreeNode(normal='')
            #[..., '^', '|']
            elif result3[-1].meta != '':
                left_child = ParseTreeNode(normal='')
            else:
                left_child = ParseTreeNode(normal='')


            #[..., '|']
            if i+1 == len(result2):
                right_child = ParseTreeNode(normal='')
            #[..., '|', '|']
            elif result2[i+1].meta != '':
                right_child = ParseTreeNode(normal='')
            else:
                right_child = result2[i+1]
                i += 1

            result3.append(ParseTreeNode(children=[left_child, right_child],
                                         operation='|')) 

        else:
            result3.append(result2[i])

    if len(result3) != 1:
        raise Exception("regex_object_list was not processed fully")

    return result3[0]

class ParseTree:
    def __init__(self, regex):
        pass

    def parse(self, regex):
        pass

if __name__ == '__main__':
    pass
