
# coding: utf-8

# # The command line tool
# 
# The winproxy command line tool parses the parameter using the argparse module.

# In[ ]:

import argparse


# In[ ]:

def cmd_view(args):
    """The view command displays the current proxy settings"""
    print('view')


# In[ ]:

def cmd_add(args):
    """The add command adds the current proxy settings to the database"""
    print('add')


# In[ ]:

def cmd_set(args):
    """Change the current proxy settings"""
    print('set')


# In[ ]:

def cmd_winproxy():
    """The command line function"""
    # Create a parser
    parser = argparse.ArgumentParser()
    
    # The command will accept subparsers
    cmd_parsers = parser.add_subparsers(dest='command', help='Get help on command')

    # The following commands are available through their subparsers
    parser_view = cmd_parsers.add_parser('view', help=cmd_view.__doc__)
    parser_view.set_defaults(func=cmd_view)
    
    parser_add = cmd_parsers.add_parser('add', help=cmd_add.__doc__)
    parser_add.set_defaults(func=cmd_add)
    
    parser_set = cmd_parsers.add_parser('set', help=cmd_set.__doc__)
    parser_set.set_defaults(func=cmd_set)

    args = parser.parse_args()
    args.func(args)

