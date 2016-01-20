
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

def cmd_cpl(args):
    """Open the windows internet settings dialog"""
    import subprocess
    subprocess.Popen(['control', 'inetcpl.cpl'])


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
    enable = args.enable
    http11 = args.http11
    server = {}
    override = args.override
    if args.proxy:
        server['all'] = args.proxy
    else:
        if args.http:
            server['http'] = args.http
        if args.https:
            server['https'] = args.https
        if args.ftp:
            server['ftp'] = args.ftp
        if args.socks:
            server['socks'] = args.socks
    p = ProxySetting()
    p.registry_read()
    changed = False
    if enable:
        p.enable = enable
        changed = True
    if http11:
        p.http11 = http11
        changed = True
    if server:
        p.server = server
        changed = True
    if override:
        p.override = override
        changed = True
    if changed:
        p.registry_write()
    p.display()


# In[ ]:

def cmd_view(args):
    """The view command displays the current proxy settings"""
    p = ProxySetting()
    p.registry_read()
    p.display(args.max_overrides)


# In[ ]:

def _to_bool(value):
    try:
        i = int(value)
        return i == 1
    except:
        if value in ['True', 'true', 'yes']:
            return True
        if value in ['False', 'false', 'no']:
            return False
        raise Exception('Can\'t convert {0} to a boolean value'.format(value))


# In[ ]:

def winproxy():
    """The command line function"""
    # Create a parser
    parser = argparse.ArgumentParser(prog='winproxy')
    
    # The command will accept subparsers
    cmd_parsers = parser.add_subparsers(dest='command', help='Get help on command')

    # The following commands are available through their subparsers
    parser_add = cmd_parsers.add_parser('add', help=cmd_add.__doc__)
    parser_add.set_defaults(func=cmd_add)
    
    parser_cpl = cmd_parsers.add_parser('cpl', help=cmd_cpl.__doc__)
    parser_cpl.set_defaults(func=cmd_cpl)
    
    parser_del = cmd_parsers.add_parser('del', help=cmd_del.__doc__)
    parser_del.set_defaults(func=cmd_del)
    
    parser_edit = cmd_parsers.add_parser('edit', help=cmd_edit.__doc__)
    parser_edit.set_defaults(func=cmd_edit)
    
    parser_off = cmd_parsers.add_parser('off', help=cmd_off.__doc__)
    parser_off.set_defaults(func=cmd_off)
    
    parser_on = cmd_parsers.add_parser('on', help=cmd_on.__doc__)
    parser_on.set_defaults(func=cmd_on)
    
    parser_set = cmd_parsers.add_parser('set', help=cmd_set.__doc__)
    parser_set.add_argument('--enable', '-e', type=_to_bool)
    parser_set.add_argument('--http11', type=_to_bool)
    parser_set.add_argument('--override', '-o', default=[], nargs='*')
    parser_set.add_argument('--all', dest='proxy', default='')
    parser_set.add_argument('--http', dest='http', default='')
    parser_set.add_argument('--https', dest='https', default='')
    parser_set.add_argument('--ftp', dest='ftp', default='')
    parser_set.add_argument('--socks', dest='socks', default='')
    parser_set.set_defaults(func=cmd_set)

    parser_view = cmd_parsers.add_parser('view', help=cmd_view.__doc__)
    parser_view.add_argument('--max-overrides', '-n', type=int, default=None, help='Limit the number of displayed proxy overrides')
    parser_view.set_defaults(func=cmd_view)
    
    args = parser.parse_args()
    try:
        # Python 3 does not display usage if command is ommitted
        # Hence, we force it...
        if not args.command:
            raise AttributeError
        args.func(args)
    except AttributeError:
        parser.print_usage()

