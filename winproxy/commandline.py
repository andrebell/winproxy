
# coding: utf-8

# # The command line tool
# 
# The winproxy command line tool parses the parameter using the argparse module.

# In[ ]:

import argparse
from . import ProxySetting


# In[ ]:

def cmd_add(args):
    """The add command adds the current proxy settings to the database"""
    print('Adding to database is not yet implemented')


# In[ ]:

def cmd_del(args):
    """Remove a particular proxy setting from the database"""
    print('Removing from database is not yet implemented')


# In[ ]:

def cmd_edit(args):
    """Open the Windows proxy settings dialog"""
    print('Opening the windows proxy settings dialog is not yet implemented')


# In[ ]:

def cmd_off(args):
    """Disable the proxy"""
    p = ProxySetting()
    p.registry_read()
    p.enable = False
    p.registry_write()


# In[ ]:

def cmd_on(args):
    """Enable the proxy"""
    p = ProxySetting()
    p.registry_read()
    p.enable = True
    p.registry_write()


# In[ ]:

def cmd_set(args):
    """Change the current proxy settings"""
    print('Changing the current settings is not yet implemented')


# In[ ]:

def cmd_view(args):
    """The view command displays the current proxy settings"""
    p = ProxySetting()
    p.registry_read()
    p.display(args.max_overrides)


# In[ ]:

def winproxy():
    """The command line function"""
    # Create a parser
    parser = argparse.ArgumentParser()
    
    # The command will accept subparsers
    cmd_parsers = parser.add_subparsers(dest='command', help='Get help on command')

    # The following commands are available through their subparsers
    parser_add = cmd_parsers.add_parser('add', help=cmd_add.__doc__)
    parser_add.set_defaults(func=cmd_add)
    
    parser_del = cmd_parsers.add_parser('del', help=cmd_del.__doc__)
    parser_del.set_defaults(func=cmd_del)
    
    parser_edit = cmd_parsers.add_parser('edit', help=cmd_edit.__doc__)
    parser_edit.set_defaults(func=cmd_edit)
    
    parser_off = cmd_parsers.add_parser('off', help=cmd_off.__doc__)
    parser_off.set_defaults(func=cmd_off)
    
    parser_on = cmd_parsers.add_parser('on', help=cmd_on.__doc__)
    parser_on.set_defaults(func=cmd_on)
    
    parser_set = cmd_parsers.add_parser('set', help=cmd_set.__doc__)
    parser_set.set_defaults(func=cmd_set)

    parser_view = cmd_parsers.add_parser('view', help=cmd_view.__doc__)
    parser_view.add_argument('--max-overrides', '-n', type=int, default=None, help='Limit the number of displayed proxy overrides')
    parser_view.set_defaults(func=cmd_view)
    
    args = parser.parse_args()
    args.func(args)

