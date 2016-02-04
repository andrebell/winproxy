
# coding: utf-8

# # The command line tool
# 
# The winproxy command line tool uses [click](https://pypi.python.org/pypi/click) to parse options, arguments and the subcommand structure.

# In[ ]:

import click
import sys
import yaml


# In[ ]:

from winproxy import ProxySetting, _SUBKEYS, _PROXYENABLE, _PROXYHTTP11, _PROXYSERVER, _PROXYOVERRIDE


# In[ ]:

reg_file_template = """Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings]
"MigrateProxy"=dword:00000001
"ProxyEnable"=dword:{ProxyEnable:08}
"ProxyHttp1.1"=dword:{ProxyHttp11:08}
"ProxyServer"="{ProxyServer}"
"ProxyOverride"="{ProxyOverride}"
"""


# In[ ]:

@click.group()
@click.version_option(prog_name='winproxy')
@click.option('--database', '-d', 'identifier', metavar='<identifier>', default=None)
@click.pass_context
def winproxy(ctx, identifier):
    """The command line function"""
    if identifier is None:
        p = ProxySetting()
        p.registry_read()
        ctx.obj = p
    else:
        p = ProxySetting()
        ctx.obj = p


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

def _export_yaml(p):
    p.override = p.override
    d = {
        _PROXYENABLE: p.enable,
        _PROXYHTTP11: p.http11,
        _PROXYSERVER: p.server,
        _PROXYOVERRIDE: p.override
    }
    return yaml.dump(d, default_flow_style=False)


# In[ ]:

def _export_reg(p):
    return reg_file_template.format(
        ProxyEnable = p[_PROXYENABLE],
        ProxyHttp11 = p[_PROXYHTTP11],
        ProxyServer = p[_PROXYSERVER],
        ProxyOverride = p[_PROXYOVERRIDE]
    )


# In[ ]:

def _export_plain(p):
    return unicode(p._registry)


# In[ ]:

@winproxy.command(name='export')
@click.option('--format', '-f', 'format', type=click.Choice(['reg', 'yaml', 'plain']), default='reg')
@click.pass_obj
def _export(p, format):
    try:
        export_func = globals()['_export_{0}'.format(format)]
    except:
        raise Exception('No such export format!')
    
    p.override = p.override
    click.echo(export_func(p))


# In[ ]:

@winproxy.command(name='off')
def _off(p):
    """Disable the proxy"""
    # Currently not working on the context object, since the write
    # operation is not bound to the corresponding source!
    p = ProxySetting()
    p.registry_read()
    p.enable = False
    p.registry_write()


# In[ ]:

@winproxy.command(name='on')
def _on(p):
    """Enable the proxy"""
    # Currently not working on the context object, since the write
    # operation is not bound to the corresponding source!
    p = ProxySetting()
    p.registry_read()
    p.enable = True
    p.registry_write()


# In[ ]:

def _reg_export(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    
    p = ctx.obj
    click.echo(_export_reg(p))


# In[ ]:

#@click.option('--output-file', '-of', 'outputfile', type=Click.File('w'))

@winproxy.command(name='reg')
@click.option('--export', '-e', default=False, is_flag=True, callback=_reg_export, expose_value=False, is_eager=True)
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
@click.pass_obj
def _view(p, max_overrides):
    """The view command displays the current proxy settings"""
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

