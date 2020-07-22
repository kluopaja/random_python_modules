#!/usr/bin/env python
import sys
"""Module for reading command line arguments


Loosely follows the POSIX.1-2017 guidelines: 
https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html

The command line arguments should consist of options, option-arguments,
operands and a special argument --

Options have to be single alphanumeric characters. Some options are followed
by option-arguments. Option-arguments are not optional. So if a option O
can be followed by an option-argument, then it must always be followed by 
an option-argument. The property of having an option-argument is defined in
option_types dict.
    
    If 'utility_name -A a' is valid and 'a' is an option-argument,
    then 'utility_name -A' is not valid

Option-arguments are strings which must not start with -.

Operands are strings which usually must not with - (see next paragraph).

After first -- argument every following argument is treated as an operand.
This means that operands can also start with - if they are placed after --.

Before the first -- or in absence of --
    1. Arguments starting with - are treated as strings of option characters
    2. Every option should be in the option_types dict
    3. Only options without option-arguments may be concatenated i.e. -abc

    4. An option (with or without option-arguments) may occur many times but only 
       the first occurrence is considered. Each of these repeats should be followed by
       an option-argument if the option requires it.
    5. If an argument is not an option or option-argument, then it is handled as a 
       operand.

Usage
-----

Simply call read. For example:
    option_values, operands = read(sys.argv, ['a', 'b'], ['c', 'd'])

Now option_values will be a dict of read options and possible corresponding values.
Value == None for options without arguments. Operands is a list of operands.

"""
def read(argv, options_without_arguments=[], options_with_arguments=[]):
    """Read options from an argv list.

        Parameters
        ----------
            argv : list (str)
                Content of sys.argv.
                Command line arguments to be read.
                
            options_without_arguments: list (str)
                Elements are single alphanumeric characters
            options_with_arguments: list (str)
                Elements are single alphanumeric characters

            Every alphanumeric character should occur at most once 
            and only in one of the lists

        Returns
        -------
        (option_values, operands)
            option_values : dict (str: str)
                Read options and possible corresponding values. Value == None
                for options without arguments

            operands : list (str)
                Read operands
    """

    #check that argv is an output of sys.argv
    check_command_line_argument_validity(argv)

    #construct a dict from the option lists
    option_types = make_option_dict(options_without_arguments, options_with_arguments)

    return parse_command_line_arguments(argv, option_types)


def make_option_dict(options_without_arguments, options_with_arguments):
    """Construct a option dict from two lists of options

    """
    options = {}
    for x in options_without_arguments:
        if x in options:
            raise ValueError("Multiple definitions of the same option")
        options[x] = 'no_option_argument'
    for x in options_with_arguments:
        if x in options:
            raise ValueError("Multiple definitions of the same option")
        options[x] = 'option_argument'

    check_option_dict_validity(options)
    return options

def check_option_dict_validity(option_types):
    """Checks the validity of options and option arguments

    Option set is valid only if:
        1. Type of every element of 'options' is correct
        2. Every option name is an alphanumeric character
        3. Every option-argument belongs to the set ['option_argument', 'no_option_argument']

    Parameters
    ----------
    options : dict ('str', 'str')
        
        Key is the value of the option. 
        Value is 'option_argument' if the option has an option-argument
        'no_option_argument' for an option without an option-argument.


    """
    for key, value in option_types.items():
        if not isinstance(key, str):
            ok = False
            raise TypeError("Option name not string")
        if len(key) != 1:
            raise ValueError("Option name not a single character")
        if not key.isalnum():
            raise ValueError("Option name not alphanumeric")
        #NOTE
        #How to handle this? The user should never set these values
        if value not in ['option_argument', 'no_option_argument']:
            raise Exception("Internal error in option list processing")




def check_command_line_argument_validity(argv):
    """Basic sanity check for argv.

    1. argv is list of string
    2. len(argv) > 0
    3. For every element s (except the first one) should hold len(s) > 0
    Parameters
    ----------
    argv : list of strings
        Content of sys.argv
        Command line arguments to be checked.
    
    Returns
    -------
    ok : bool
        True if no errors were detected
        False if argv is not a valid argument list

    TODO
    ----
    Should only raise exceptions and not return anything

    """
    ok = True
    #must be a list
    if not isinstance(argv, list):
        return False

    for x in argv:
        if not isinstance(x, str):
            return False


    #must always at least contain the program name
    if len(argv) < 1:
        ok = False

    #apart from the program name, every other argument must be nonempty
    for i in range(1, len(argv)):
        if len(argv[i]) == 0:
            ok = False

    return ok

def parse_command_line_arguments(argv, option_types):
    """Extract options and operands from the argv.

    Parameters
    ----------
    argv : list of strings
        Content of sys.argv
        First element is the program name
        For subsequent elements s should hold |s| > 0
    
    option_types : dict (str: str)
        Key is the value of the option. 
        Value is 'option_argument' if the option has an option-argument
        'no_option_argument' for an option without an option-argument.
    
    Returns
    -------
    (argv_options, operands) : tuple
        argv_options : dict (str: (None | str))
            Options with their corresponding option-arguments or None
        operands : list (str)
    
    """

    
    #options encountered in the argv
    #for options without option-arguments (c, None) is added
    #for option with option-arguments (c, d) is added where 
    #where c is the option and d is the option-argument
    argv_options = {}    

    #list of strings
    operands = []


    #will be switched to True if -- is encountered 
    only_operands = False
    #we can skip the first argument which is the file name
    #and should be correct
    pos = 1
    while pos < len(argv):
        #after first --, every argv[i] is an operand
        if only_operands:
            operands.append(argv[pos])
        else:
            #which to only operands mode if -- is encountered
            if argv[pos] == '--':
                only_operands = True

            #if new argument start with -, then it is an option
            elif argv[pos][0] == '-':



                    #if at least one of the options has arguments
                    has_argument = False
                    for i in range(1, len(argv[pos])):
                        if argv[pos][i] not in option_types:
                            raise ValueError(f"Option {argv[pos]} not valid")
                        #if the option argv[i] requires an option-argument
                        if option_types[argv[pos][i]] == 'option_argument':
                            has_argument = True

                    #option cannot be empty
                    if len(argv[pos]) == 1:
                        raise ValueError(f'Option cannot be empty (only -)')

                    if has_argument:
                        if len(argv[pos]) == 2:
                            #check that there is a option-argument in argv
                            if pos + 1 >= len(argv):
                                raise ValueError(f'No option-argument was provided for: {argv[pos]}')

                            #check that the option-argument doesn't start with -
                            if argv[pos+1][0] == '-':
                                raise ValueError(f'Option-argument for {argv[pos]} starts with an illegal character: {argv[pos+1]}')

                            #only update the value if not already present
                            if argv[pos][1] not in argv_options:
                                argv_options[argv[pos][1]] = argv[pos+1]

                            #because we handled two elements
                            pos += 1
                        #options with arguments can't be concatenated
                        elif len(argv[pos]) > 2:
                            raise ValueError(f'Options with option-arguments cannot be concatenated: {argv[pos]}')
                        #we should never end up here
                        else:
                            raise ValueError()
                    #if options don't require option-arguments, just add every option to argv_options
                    else:
                        for option in argv[pos][1:]:
                            if option not in argv_options:
                                argv_options[option] = None;

            #otherwise we will just add it to the operands
            else:
                operands.append(argv[pos])

        pos += 1        
    
    return (argv_options, operands)


options_without_arguments = ['A', 'a', '1']
options_with_arguments = ['B', 'b', '2']
                     
if __name__ == "__main__":
    print("options_without_arguments: ", end='')
    print(options_without_arguments);
    print("options_with_arguments: ", end='')
    print(options_with_arguments)
    print("sys.argv: ", end='')
    print(sys.argv)
    
    result = read(sys.argv, options_without_arguments, options_with_arguments)
    print(result)
