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
        

We note that regular expressions are formed in a way that directly gives us
instructions to generate a finite automaton which recognizes the same language.

Unfortunately parsing the regular expression is complicated by a few
details:
    We include the following shorthand notations:
        (R(R*)) = (R+)
        (R|_) = (R?)

    The different operators are evaluated in the order: */+/?,
    concatenation, union.

    Operators are evaluated from left to right.

    All excessive parentheses can simply be left out.

    For example:
        (a(b(a(b(a))))) = ababa
        (a|((b*)c)) = a|b*c


"""
