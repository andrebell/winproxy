
# coding: utf-8

# # The command line tool
# 
# The winproxy command line tool uses [click](https://pypi.python.org/pypi/click) to parse options, arguments and the subcommand structure.

# In[ ]:

import click
from . import ProxySetting


# In[ ]:

# Requires getting parameters from subcommands....
# Well... To be done...
@click.group()
@click.version_option(prog_name='winproxy')
def winproxy():
    """The command line function"""
    pass
    
    ##############################################################
    ## argparse structure
    ##############################################################
    ## Create a parser
    #parser = argparse.ArgumentParser(prog='winproxy')
    #
    ## The command will accept subparsers
    #cmd_parsers = parser.add_subparsers(dest='command', help='Get help on command')
    #
    ## The following commands are available through their subparsers
    #parser_add = cmd_parsers.add_parser('add', help=cmd_add.__doc__)
    #parser_add.set_defaults(func=cmd_add)
    #
    #parser_cpl = cmd_parsers.add_parser('cpl', help=cmd_cpl.__doc__)
    #parser_cpl.set_defaults(func=cmd_cpl)
    #
    #parser_del = cmd_parsers.add_parser('del', help=cmd_del.__doc__)
    #parser_del.set_defaults(func=cmd_del)
    #
    #parser_edit = cmd_parsers.add_parser('edit', help=cmd_edit.__doc__)
    #parser_edit.set_defaults(func=cmd_edit)
    #
    #parser_off = cmd_parsers.add_parser('off', help=cmd_off.__doc__)
    #parser_off.set_defaults(func=cmd_off)
    #
    #parser_on = cmd_parsers.add_parser('on', help=cmd_on.__doc__)
    #parser_on.set_defaults(func=cmd_on)
    #
    #parser_set = cmd_parsers.add_parser('set', help=cmd_set.__doc__)
    #parser_set.add_argument('--enable', '-e', type=_to_bool)
    #parser_set.add_argument('--http11', type=_to_bool)
    #parser_set.add_argument('--override', '-o', default=[], nargs='*')
    #parser_set.add_argument('--all', dest='proxy', default='')
    #parser_set.add_argument('--http', dest='http', default='')
    #parser_set.add_argument('--https', dest='https', default='')
    #parser_set.add_argument('--ftp', dest='ftp', default='')
    #parser_set.add_argument('--socks', dest='socks', default='')
    #parser_set.set_defaults(func=cmd_set)
    #
    #parser_view = cmd_parsers.add_parser('view', help=cmd_view.__doc__)
    #parser_view.add_argument('--max-overrides', '-n', type=int, default=None, help='Limit the number of displayed proxy overrides')
    #parser_view.set_defaults(func=cmd_view)
    #
    #args = parser.parse_args()
    #try:
    #    # Python 3 does not display usage if command is ommitted
    #    # Hence, we force it...
    #    if not args.command:
    #        raise AttributeError
    #    args.func(args)
    #except AttributeError:
    #    parser.print_usage()


# In[ ]:

@winproxy.command(name='add')
def _add():
    """The add command adds the current proxy settings to the database"""
    click.echo('Adding to database is not yet implemented')


# In[ ]:

@winproxy.command(name='cpl')
def _cpl():
    """Open the windows internet settings dialog"""
    #click.launch('control inetcpl.cpl')
    import subprocess
    subprocess.Popen(['control', 'inetcpl.cpl'])


# In[ ]:

@winproxy.command(name='del')
def _del():
    """Remove a particular proxy setting from the database"""
    click.echo('Removing from database is not yet implemented')


# In[ ]:

@winproxy.command(name='edit')
def _edit():
    """Open the Windows proxy settings dialog"""
    click.echo('Opening the windows proxy settings dialog is not yet implemented')


# In[ ]:

@winproxy.command(name='off')
def _off():
    """Disable the proxy"""
    p = ProxySetting()
    p.registry_read()
    p.enable = False
    p.registry_write()


# In[ ]:

@winproxy.command(name='on')
def _on():
    """Enable the proxy"""
    p = ProxySetting()
    p.registry_read()
    p.enable = True
    p.registry_write()


# In[ ]:

@winproxy.command(name='server')
@click.argument('serversetting', default=None, required=False)
def _server(serversetting):
    """Experimental command to read or set the ProxyServer property directly."""
    p = ProxySetting()
    p.registry_read()
    if serversetting is None:
        click.echo(p._server[0])
    else:
        p._server = (serversetting, p._server[1])
        p.registry_write()


# In[ ]:

@winproxy.command(name='set')
@click.option('--enable/--disable', '-e/-d', 'enable', default=None)
@click.option('--http11/--no-http11', '-h/-nh', 'http11', default=None)
@click.option('--override', '-o', default=None) #, nargs='*')
@click.option('--all', 'proxy', default=None)
@click.option('--http', default=None)
@click.option('--https', default=None)
@click.option('--ftp', default=None)
@click.option('--socks', default=None)
def _set(enable, http11, override, proxy, http, https, ftp, socks):
    """Change the current proxy settings"""
    server = None
    if not proxy is None and not proxy == '':
        server = dict(all=proxy)
    else:
        server = {}
        if not http is None and not http == '':
            server['http'] = http
        if not https is None and not https == '':
            server['https'] = https
        if not ftp is None and not ftp == '':
            server['ftp'] = ftp
        if not socks is None and not socks == '':
            server['socks'] = socks
        if server == {}:
            server = None
    click.echo(server)
    
    p = ProxySetting()
    p.registry_read()
    
    changed = False
    if not enable is None:
        p.enable = enable
        changed = True
    if not http11 is None:
        p.http11 = http11
        changed = True
    if not server is None:
        p.server = server
        changed = True
    if not override is None:
        p.override = override
        changed = True
    if changed:
        p.registry_write()


# In[ ]:

@winproxy.command(name='view')
@click.option('--max-overrides', '-n', 'max_overrides', help='Limit the number of displayed proxy overrides') #type=int, default=None, 
def _view(max_overrides):
    """The view command displays the current proxy settings"""
    p = ProxySetting()
    p.registry_read()
    
    click.echo("ProxyEnable: {0}".format(p.enable))
    click.echo("ProxyHttp11: {0}".format(p.http11))
    click.echo("ProxyServer: {0}".format(p._server[0]))
    if max_overrides == 0:
        # Do not display proxy overrides
        pass
    else:
        # Display proxy overrides, possibly limited number
        click.echo("ProxyOverride:")

        if max_overrides == None or max_overrides == -1:
            displayed_overrides = p.override
            limited = False
        else:
            displayed_overrides = p.override[:max_overrides]
            limited = True

        for exc in displayed_overrides:
            click.echo("- {0}".format(exc))

        if limited and (len(p.override)-max_overrides > 0):
            click.echo("- ... ({0} more)".format(len(p.override)-max_overrides))

