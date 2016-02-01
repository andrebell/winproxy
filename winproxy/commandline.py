
# coding: utf-8

# # The command line tool
# 
# The winproxy command line tool uses [click](https://pypi.python.org/pypi/click) to parse options, arguments and the subcommand structure.

# In[ ]:

import click
import sys

from . import ProxySetting, _SUBKEYS, _PROXYSERVER


# In[ ]:

@click.group()
@click.version_option(prog_name='winproxy')
def winproxy():
    """The command line function"""
    pass


# @winproxy.command(name='add')
# def _add():
#     """The add command adds the current proxy settings to the database"""
#     click.echo('Adding to database is not yet implemented')

# In[ ]:

@winproxy.command(name='cpl')
def _cpl():
    """Open the windows internet settings dialog"""
    #click.launch('control inetcpl.cpl')
    import subprocess
    subprocess.Popen(['control', 'inetcpl.cpl'])


# @winproxy.command(name='del')
# def _del():
#     """Remove a particular proxy setting from the database"""
#     click.echo('Removing from database is not yet implemented')

# @winproxy.command(name='edit')
# def _edit():
#     """Open the Windows proxy settings dialog"""
#     click.echo('Opening the windows proxy settings dialog is not yet implemented')

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

@winproxy.command(name='reg')
@click.argument('subkey', default='ProxyServer')
@click.argument('value', default=None, required=False)
def _reg(subkey, value):
    """Experimental command to read or set the ProxyServer property directly."""
    subkey_map = dict(zip(map(lambda s: s.lower(), _SUBKEYS), _SUBKEYS))
    subkey = subkey_map.get(subkey.lower(), None)
    if subkey is None:
        click.echo(
            click.style(
                "Error! Invalid registry key specified.",
                fg='red', bold=True
            )
        )
        sys.exit(1)
    
    p = ProxySetting()
    p.registry_read()
    
    if value is None:
        # Display current value
        value = p[subkey]
        click.echo("{0}: {1}".format(subkey, value))
    else:
        p[subkey] = value
        p.registry_write()


# In[ ]:

@winproxy.command(name='set')
@click.option('--enable/--disable', '-e/-d', 'enable', default=None)
@click.option('--http11/--no-http11', '-h/-nh', 'http11', default=None)
@click.option('--override', '-o', default=None) #, nargs='*')
@click.option('--all', '-a', 'proxy', default=None)
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
@click.option('--max-overrides', '-n', 'max_overrides', type=int, default=None,
              help='Limit the number of displayed proxy overrides')
def _view(max_overrides):
    """The view command displays the current proxy settings"""
    p = ProxySetting()
    p.registry_read()
    
    click.echo("ProxyEnable: {0}".format(p.enable))
    click.echo("ProxyHttp11: {0}".format(p.http11))
    # Display ProxyServer in raw format
    click.echo("ProxyServer: {0}".format(p[_PROXYSERVER]))
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


# In[ ]:

@winproxy.command(name='new')
@click.argument('optarg', default=None, required=False)
def _new(optarg):
    if optarg is None:
        click.echo('None')
    else:
        click.echo(optarg)

