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
defined? How to prove this?

To parse these we first form a tree just based on the parentheses.
To be continued...

"""
class NFANode:
    """Class for NFA nodes.

    Id of a node is always its index in NFA.nodes

    Attributes
    ----------

    self.transitions : dict (str, set)
        set of nodes reachable from self with the key

    """
    def __init__(self, transitions={}):
        self.transitions = copy.deepcopy(transitions)

    def add_transition(self, target, symbol):
        if symbol in self.transitions:
            self.transitions[symbol].add(target)
        else:
            self.transitions[symbol] = {target}

    def transitions_with_symbol(self, symbol):
        if symbol in self.transitions:
            return list(self.transitions[symbol])
        else:
            return []

#TODO can be removed
    def transition_list(self):
        """Returns list of transitions from self

        Returns
        -------
            result : list of tuples
                result[i][0]: end
                result[i][1]: symbol
        """

        result = []
        for symbol, target in self.transitions.items():
                result.append((target, symbol))

        return result


    def copy(self):
        return NFANode(self.transitions)

class NFA:
    """Implements non-deterministic finite automaton

    Attributes
    ----------


    Notes
    -----
    The NFA objects can internally be in two states: compiled and not compiled.
    Compilation refers to generating a list of NFANode objects according
    to the self.transitions. The generated list of NFANode objects can then
    be used to evaluate the NFA.

    The rationale behind compilation is that the list of transitions is easier
    to handle when performing operations on NFAs (concatenation, union, ...)
    but the list of NFANodes is easier to handle when evaluating the NFA.
    """
    def __init__(self, n_nodes, start_node, accepted_nodes, transitions):
        self.n_nodes = n_nodes
        self.start_node = start_node
        self.accepted_nodes = accepted_nodes.copy()
        self.transitions = transitions.copy()

        self.compiled = False
        self.nodes = None
    @classmethod
    def union_of_characters(cls, characters):
        """Construct a small NFA for a set of characters

        Parameters
        ----------
        characters : list(str)

        """
        transitions = [(0, 1, x) for x in characters]
        return NFA(2, 0, 1, transitions)

    def evaluate(self, s):
        """Determine if the NFA accepts string s
        """
        if not compiled:
            self.compile()

        node_list = [self.start_node]

        node_list = reachable_with_empty(node_list)

        for i in range(len(s)):
            node_list = reachable_with_symbol(node_list, s[i])
            node_list = reachable_with_empty(node_list)

        for x in node_list:
            if x in self.accepted_nodes:
                return True

        return False

    def reachable_with_symbol(self, node_list, symbol):
        """Returns states which are reachable with symbol. See Notes.

        Parameters
        ----------
        node_list : list (int)

        symbol : str

        Returns
        -------
        new_node_list : list (int)

        Notes
        -----
        This function always traverses edges in the tree. So calling this
        with symbol='' and node x will NOT return the node x unless x is
        part of a cycle of '' edges. Compare with reachable_with_empty.

        """

        new_node_list = []
        id_active = [False for i in range(self.n_nodes)]

        for i in range(len(node_list)):
            node_id = node_list[i]
            neighbours = self.nodes[node_id].transitions_with_symbol(symbol)
            for x in neighbours:
                if not id_active[x]:
                    new_node_list.append(x)
                    id_active[x] = True

        return new_node_list

    def reachable_with_empty(self, node_list):
        """Returns states that are reachable without consuming any symbols.

        Parameters
        ----------
        node_list : list (int)

        symbol : str

        Returns
        -------
        new_node_list : list(int)

        Notes
        -----
        Also returns every node in node_list. Compare with
        reachable_with_symbol.
        """

        new_node_list = reachable_with_symbol(node_list, '')
        #it is not necessary to use the empty string edges
        new_node_list.extend(node_list)
        #remove duplicates
        new_node_list = list(set(new_node_list))
        return new_node_list

    def copy(self):
        return NFA(self.n_nodes, self.start_node, self.accepted_nodes,
                  self.transitions)

    def compile(self):
        """Construct a graph of NFANodes with transitions from self.transitions

        """
        self.nodes = [NFANode() for i in range(self.n_nodes)]
        self.process_transitions()
        self.compiled = True

    def process_transitions(self):
        """Adds transitions to node objects

        """
        for x in self.transitions:
            self.nodes[x[0]].add_transition(x[1], x[2])

    def apply_offset(self, offset):
        """Shifts _all_ indexes by offset.

        Parameters
        ----------
            offset : non-negative integer

        Notes
        -----
        Used to make the nodes in two graphs non-overlapping.

        """

        self.compiled = False

        if offset < 0:
            raise ValueError("offset cannot be negative")

        self.n_nodes += offset
        self.start_node += offset

        for i in range(len(self.transitions)):
            self.transitios[i][0] += offset
            self.transitios[i][1] += offset

    def union(self, other):
        """Return union as a new NFA
        """
        self_copy = self.copy()
        other_copy = other.copy()
        #make the node ids non-overlapping
        other_copy.apply_offset(self_copy.n_nodes)

        self_copy.n_nodes += other_copy.n_nodes
        self_copy.transitions.extend(other_copy.transitions)

        self_old_start = self_copy.start_node
        other_old_start = other_copy.start_node

        #set new start node
        self_copy.n_nodes += 1
        self_copy.start_node = self_copy.n_nodes-1

        #add edges from the new start node
        new_edges = []
        new_edges.append((self_copy.start_node, self_old_start, ''))
        new_edges.append((self_copy.start_node, other_old_start, ''))
        self_copy.transitions.extend(new_edges)

        #update accepted nodes
        self_copy.accepted_nodes.extend(other_copy.accepted_nodes)

        return self_copy

    def concatenate(self, other):
        """Return concatenation as a new NFA

        """
        self_copy = self.copy()
        other_copy = other.copy()

        #make sure the node ids are not overlapping
        other_copy.apply_offset(self_copy.n_nodes)

        self_copy.n_nodes += other_copy.n_nodes
        self_copy.add_transitions(other_copy.transitions)

        new_edges = []
        for x in self_copy.accepted_nodes:
            new_edges.append((x, other_copy.start_node, ''))


        self_copy.transitions.extend(new_edges)
        self_copy.accepted_nodes = other_copy.accepted_nodes.copy()

        return self_copy

    def star(self):
        """Return a new NFA self*

        """
        self_copy = self.copy()

        #add new start node and add it to accepted nodes
        self_copy.n_nodes += 1
        self_new_start = self_copy.n_nodes-1

        self_copy.accepted_nodes.append(self_new_start)

        #add edges from the accepted states to the old start node
        new_edges = []
        for x in self_copy.accepted_nodes:
            new_edges.append((x, self_copy.start_node, ''))

        self_copy.transitions.extend(new_edges)

        self_copy.start_node = self_new_start

        return self_copy

    def plus(self):
        """Return a new NFA self+ = selfself*
        """

        return self.concatenate(self.star())

    def question(self):
        """Return a new set self? = (_|self)
        """
        return self.union(NFA.union_of_characters(['']))

class ParseTreeNode:
    """Used to represent the regex as a tree

    Attributes
    ----------
    self.children : list (ParseTreeNode)

    self.meta : str or None
        regex metacharacter (e.g. '*+?()|.')

        Every character that is not directly representing a character of the
        mached string.

        Only '.' should be present in the final tree (leafs only)

    self.normal : str or None
        normal character(s)

        If len(self.normal) > 1, then union of the characters
        #NOTE: should this depend on the self.operation?

        Should be nonempty only in the leaves of the final tree

    self.operation : str or None
        operation applied to self.children

        only in the inner nodes of the final tree

    Also used during the parsing process when the regex is represented
    """
    def __init__(self, children=[], meta=None, normal=None, operation=None):
        self.children = children
        #meta and normal are used for leaves
        self.meta = meta
        self.normal = normal

        #TODO check that the constructed node is valid!
        #TODO modify the @final tree@

        #operation is used for internal nodes in the final tree
        self.operation = operation

    def __eq__(self, other):
        if not isinstance(other, ParseTreeNode):
            return NotImplemented

        if self.meta != other.meta or self.normal != other.normal \
           or self.operation != other.operation:
            return False

        if len(self.children) != len(other.children):
            return False

        for i in range(len(self.children)):
            if self.children[i] != other.children[i]:
                return False

        return True

    def __repr__(self):
        self_repr = "("
        self_repr += ", ".join([str(self.operation),
                                str(self.meta),
                                str(self.normal)])
        self_repr += ")"
        if len(self.children) == 0:
            return self_repr
        return self_repr + repr(self.children)

    def __str__(self):
        """Prints tree in a user friendly format.

        The state of the current node is expressed by three consecutive
        characters. Let the characters be 'ABC'. Now self.operation == 'A',
        self.meta = 'B' and self.normal = 'C'. None is denoted by 'N'.
        Empty self.normal is denoted by '_'
        """
        rows = self.str_helper(level_depth=3)
        return '\n'.join(rows)

    def str_helper(self, level_depth=0):
        """Returns list of rows of the text presentation of the tree

        Parameters
        ----------
            level_depth: integer (>=0)
                extra space between subsequent tree levels
        """
        if level_depth < 0:
            raise ValueError("level_depth must be nonnegative")

        prefix = 'N' if self.operation is None else self.operation[0]
        prefix += 'N' if self.meta is None else self.meta[0]
        if self.normal is None:
            prefix += 'N'
        elif self.normal is '':
            prefix += '_'
        else:
            prefix += self.normal[0]

        if len(self.children) == 0:
            return [prefix]

        out = []
        child_strs = [x.str_helper(level_depth) for x in self.children]
        for i in range(len(child_strs)):
            for j in range(len(child_strs[i])):
                if i == 0 and j == 0:
                    prefix += "-"*level_depth
                elif j == 0:
                    prefix = "+--"
                    prefix += "-"*level_depth
                elif i != len(child_strs)-1:
                    prefix = "|  "
                    prefix += " "*level_depth
                else:
                    prefix = "   "
                    prefix += " "*level_depth

                out.append(prefix+child_strs[i][j])
                if j == len(child_strs[i])-1 and i != len(child_strs)-1:
                    out.append('|')

        return out

def parse_regex(regex):
    """Generates parse tree from regex

    Parameters
    ----------
    regex : str


    Returns
    -------
    root : ParseTreeNode
        Root of the generated parse tree corresponding to regex

    """

    tmp = regex_to_parse_tree_nodes(regex)
    root = parse_nodes_to_tree(tmp)
    return root

def regex_to_parse_tree_nodes(regex):
    """Processes a regex string for further use

    Parameters
    ----------
    regex : str


    Returns
    -------
    leafs : list (ParseTreeNode)
        ParseTree leafs to be converted to a parse tree

    Notes
    -----

    Every character (including escaped characters) is converted to a
    ParseTreeNode object.
    """

    i = 0
    leafs = []
    while i < len(regex):
        new_node = ParseTreeNode()
        if regex[i] == '\\':
            new_node.normal = regex[i+1:i+2]
            i += 2
        else:
            if regex[i] in '*+?|().':
                new_node.meta = regex[i]
            else:
                new_node.normal = regex[i]
            i += 1

        leafs.append(new_node)

    return leafs

def parse_nodes_to_tree(parse_nodes):
    """Generates parse tree from parse_nodes

    Parameters
    ----------
    parse_leafs : list of ParseTreeNodes
        Regex represented as a list of parse tree leafs

    Returns
    -------
    root : ParseTreeNode
        Root of the generated parse tree generated from parse_leafs

    Notes
    -----
    Handles parentheses in the regex and calls parse_wo_parentheses

    """

    #parse node sequences without any parentheses
    #regex_lists[i] corresponds to a substring  which is enclosed in
    #i (unprocessed) parentheses
    regex_lists = [[]]

    for i in range(len(regex_object_list)):
        if regex_object_list[i].meta == '(':
            regex_lists.append([])

        elif regex_object_list[i].meta == ')':
            if len(regex_list) <= 1:
                raise ValueError("Incorrect parentheses in regex_object_list")

            tmp = parse_wo_parentheses(regex_lists[-1])
            regex_lists[-2].append(tmp)
            regex_lists.pop()
        else:
            regex_lists[-1].append(regex_object_list[i])

    root = parse_wo_parentheses(regex_lists[0])

def parse_wo_parentheses(parse_nodes):
    """Parses a ParseTreeNode list not containing any parentheses

    Parameters
    ----------
    parse_nodes : list of characters or ParseTreeNodes
        Should not contain any parentheses

    Returns
    -------
    root : ParseTreeNode
        Root of the generated parse tree corresponding to parse_nodes

    """

    regex_object_list = process_unary(regex_object_list)
    regex_object_list = process_concatenation(regex_object_list)
    regex_object_list = process_union(regex_object_list)


    if len(regex_object_list) != 1:
        raise Exception("regex_object_list was not processed fully")

    return regex_object_list[0]

def process_unary(parse_nodes):
    """Processes nodes with a metacharacters ['*', '+', '?']

"""
    result = []

    for i in range(len(parse_nodes)):
        if parse_nodes[i].meta in ['*', '+', '?']:
            if len(result) == 0:
                raise ValueError("Nothing to repeat in front of */+/?")

            if result[-1].meta == '|':
                raise ValueError("| cannot be followed by */+/?")

            #TODO More error checking
            new_node = ParseTreeNode(children=[result[-1]],
                                     operation=parse_nodes[i].meta)

            result[-1] = new_node
        else:
            result.append(parse_nodes[i])

    return result

def process_concatenation(parse_nodes):
    result = []
    for i in range(len(parse_nodes)):
        result.append(parse_nodes[i])
        if len(result)  >= 2:
            #TODO meta == '.' or  normal is not None or something to
            #replace these
            if result[-2].meta != '|' and result[-1].meta != '|':
                new_node = ParseTreeNode(children=result[-2:],
                                         operation='concatenation')
                result[-2:] = []
                result.append(new_node)

    return result

def process_union(parse_nodes):
    result = []
    i = 0
    while i < len(parse_nodes):
        if parse_nodes[i].meta == '|':
            #in some cases we need to create empty nodes here

            #['|', ...]
            if i == 0:
                left_child = ParseTreeNode(normal='')
            #['a', '|']
            elif result[-1].normal != None or result[-1].meta in ['.'] \
                 or result[-1].operation != None:
                left_child = result.pop()
            else:
                raise Exception("Unknown metacharacter before |")

            #[..., '|']
            if i+1 == len(parse_nodes) or parse_nodes[i+1].meta == '|':
                right_child = ParseTreeNode(normal='')
            #[..., '|', 'a'] or [..., '|'
            elif parse_nodes[i+1].normal != None \
                or parse_nodes[i+1].meta in ['.'] \
                or parse_nodes[i+1].operation != None:
                right_child = parse_nodes[i+1]
                i += 1
            else:
                raise Exception("Unknown metacharacter after |")

            result.append(ParseTreeNode(children=[left_child, right_child],
                                         operation='|'))
        else:
            result.append(parse_nodes[i])
        i += 1

    return result

if __name__ == '__main__':
    pass
