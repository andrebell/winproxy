
# coding: utf-8

# # Python 2.7 compatibility
# 
# To achieve Python 2.7 compatibility we will import the "\_winreg" module
# from six.moves, since it has been renamed to winreg in Python 3.

# In[ ]:

import re, six
from six.moves import winreg


# The relevant keys in the registry may not exist at all. This will through a
# WindowsError on Python 2.7 and a FileNotFoundError on Python 3. Hence, for
# Python 2.7 we introduce the Python 3 exception name FileNotFoundError.

# In[ ]:

if six.PY2:
    FileNotFoundError = WindowsError


# All Proxy relevant keys are hold by a set of constants.

# In[ ]:

# Registry constants
_ROOT = winreg.HKEY_CURRENT_USER
_BASEKEY = 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'
_ACCESS = winreg.KEY_ALL_ACCESS
_PROXYENABLE = 'ProxyEnable'
_PROXYHTTP11 = 'ProxyHttp1.1'
_PROXYSERVER = 'ProxyServer'
_PROXYOVERRIDE = 'ProxyOverride'
_SUBKEYS = [
    _PROXYENABLE,
    _PROXYHTTP11,
    _PROXYSERVER,
    _PROXYOVERRIDE,
]


# # Proxy setting class
# 
# All access to the registry and database of proxysettings, as well as the
# application programming interface should be bound to one class calles
# ProxySetting.
# 
# There are four entries in the registry, that are used to configure the proxy
# settings:
# 
# - ProxyEnable (Proxy enabled or disabled)
# - ProxyHttp11 (Proxy use HTTP 1.1 enable or disable)
# - ProxyServer (String of all proxy servers and ports for all protocols)
# - ProxyOverride (String of all proxy exceptions)
# 
# As seen from the Python API these will be represented as Python types, i.e.
# 
# - ProxyEnable, a boolean
# - ProxyHttp11, a boolean
# - ProxyServer, a string 'server:port' if only one proxy is to be used or a
#   dictionary mapping protocol to 'server:port' setting
# - ProxyOverride, a list of proxy exceptions

# In[ ]:

class ProxySetting(object):
    def __init__(self):
        # Internal state (default empty, disabled setting) 
        self._name = None
        self._set_defaults()
    
    def __repr__(self):
        if not self.enable:
            return u'<Proxy Disabled>'
        else:
            return u"<Proxy '{0}'>".format(self._server[0])
    
    def __getitem__(self, key):
        return self._registry[key][0]
    
    def __setitem__(self, key, value):
        v, t = self._registry[key]
        if key in [_PROXYENABLE, _PROXYHTTP11]:
            if not isinstance(value, int) or value not in [0, 1]:
                raise Exception('Wrong type or value')
            self._registry[key] = (value, t)
        elif key in [_PROXYSERVER, _PROXYOVERRIDE]:
            if not isinstance(value, six.string_types):
                raise Exception('Wrong type or value')
            self._registry[key] = (value, t)
        else:
            raise Exception('Could not set value')
    
    def _set_defaults(self):
        self._registry = {
            _PROXYENABLE: (0, 4),
            _PROXYHTTP11: (1, 4),
            _PROXYSERVER: ('', 1),
            _PROXYOVERRIDE: ('', 1)
        }
        
    def registry_read(self):
        """Read values from registry"""
        proxykey = winreg.OpenKey(_ROOT, _BASEKEY, 0, _ACCESS)
        self._set_defaults()
        # If any value is not available in the registry, we fall back to the defaults
        for subkey in _SUBKEYS:
            try:
                # This will return (value, type) tuples, that are stored for each subkey
                self._registry[subkey] = winreg.QueryValueEx(proxykey, subkey)
            except FileNotFoundError:
                pass
        winreg.CloseKey(proxykey)
        # Normalize ProxyOverride to semicolon separated list
        self.override = self.override
    
    def registry_write(self):
        """Write values to registry"""
        proxykey = winreg.OpenKey(_ROOT, _BASEKEY, 0, _ACCESS)
        for subkey in _SUBKEYS:
            value, regtype = self._registry[subkey]
            winreg.SetValueEx(proxykey, subkey, 0, regtype, value)
        winreg.CloseKey(proxykey)

    @property
    def enable(self):
        """Proxy enable status"""
        return self[_PROXYENABLE] == 1
    
    @enable.setter
    def enable(self, on):
        """Set enable value from a boolean value"""
        if on:
            self[_PROXYENABLE] = 1
        else:
            self[_PROXYENABLE] = 0
    
    @property
    def http11(self):
        """Proxy http1.1 status"""
        return self[_PROXYHTTP11] == 1
    
    @http11.setter
    def http11(self, on):
        if on:
            self[_PROXYHTTP11] = 1
        else:
            self[_PROXYHTTP11] = 0
    
    @property
    def server(self):
        """Return the proxy server(s).
        
        If individual proxy servers are set, then a dictionary
        mapping protocol to proxy:port is returned, e.g.:
        
        dict(http='192.168.0.1:8000',
             https='192.168.0.1:8001')
        
        If only one proxy is used for all protocols, then a
        dictionary of the form:
        
        dict(all='192.168.0.1:8000')
        
        is returned."""
        # If protocol specific proxy settings are used, these are
        # assigned to the protocol names with the '=' sign
        proxyserver = self[_PROXYSERVER]
        if proxyserver.find('=') >= 0:
            servers = proxyserver.split(';')
            servers = dict(map(lambda p: p.split('='), servers))
        else:
            servers = dict(all=proxyserver)
        return servers
    
    @server.setter
    def server(self, proxies):
        """Set the proxy servers
        
        If proxies is a string, it will be assigned as the proxy server
        setting directly, e.g.
        
        >>> p = ProxySetting()
        >>> p.server = '192.168.0.1:8000'
        >>> p.server
        {'all': '192.168.0.1:8000'}
        >>> p.server = 'http=192.168.0.1:8000;https=192.168.0.1:8001;ftp=192.168.0.1:8002;socks=192.168.0.1:8004'
        >>> p.server
        {'ftp': '192.168.0.1:8002',
         'http': '192.168.0.1:8000',
         'https': '192.168.0.1:8001',
         'socks': '192.168.0.1:8004'}
        
        If the proxies parameter is a dictionary, the individual entries will be used.
        Allowed keys are 'http', 'https', 'ftp', and 'socks' - or - 'all'. 
        If a key 'all' is provided, it will take precedence. Example:
        
        >>> p.server = dict(all='192.168.0.1:8000')
        >>> p.server
        {'all': '192.168.0.1:8000'}
        """
        if isinstance(proxies, six.string_types):
            # TODO: Check if string is valid
            self[_PROXYSERVER] = proxies
        elif isinstance(proxies, dict):
            # Check for 'all' first
            if 'all' in proxies:
                # TODO: Check value
                self[_PROXYSERVER] = proxies['all']
            else:
                # TODO: Check validity of dict
                http = proxies.get('http', None)
                https = proxies.get('https', None)
                ftp = proxies.get('ftp', None)
                socks = proxies.get('socks', None)
                proxy_list = []
                if http:
                    proxy_list.append('http={0}'.format(http))
                if https:
                    proxy_list.append('https={0}'.format(https))
                if ftp:
                    proxy_list.append('ftp={0}'.format(ftp))
                if socks:
                    proxy_list.append('socks={0}'.format(socks))
                # This one even works with the empty list
                self[_PROXYSERVER] = ';'.join(proxy_list)
        else:
            # TODO: Provide Exception-classes
            raise Exception('Wrong proxy type')
    
    @property
    def override(self):
        """Return a list of all proxy exceptions"""
        return [e.strip() for e in re.split(';|,', self[_PROXYOVERRIDE]) if e.strip() != '']
    
    @override.setter
    def override(self, overridelist):
        """Set the override value from a list of proxy exceptions"""
        # TODO: Add some check on validity of input
        self[_PROXYOVERRIDE] = ';'.join(overridelist)

