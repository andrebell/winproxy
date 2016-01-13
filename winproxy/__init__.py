
# coding: utf-8

# In[ ]:

import six
from six.moves import winreg

# Registry constants
_ROOT = winreg.HKEY_CURRENT_USER
_BASEKEY = 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'
_ACCESS = winreg.KEY_ALL_ACCESS
_PROXYENABLE = 'ProxyEnable'
_PROXYHTTP11 = 'ProxyHttp1.1'
_PROXYSERVER = 'ProxyServer'
_PROXYOVERRIDE = 'ProxyOverride'


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
        self._enable = (0, 4)
        self._http11 = (1, 4)
        self._server = ('', 1)
        self._override = ('', 1)
    
    def __repr__(self):
        if not self.enable:
            return u'<Proxy Disabled>'
        else:
            return u"<Proxy '{0}'>".format(self._server[0])
    
    def display(self, max_overrides=5):
        print("ProxyEnable: {0}".format(self.enable))
        print("ProxyHttp11: {0}".format(self.http11))
        print("ProxyServer: {0}".format(self._server[0]))
        if max_overrides == 0:
            # Do not display proxy overrides
            pass
        else:
            # Display proxy overrides, possibly limited number
            print("ProxyOverride:")

            if max_overrides == None or max_overrides == -1:
                displayed_overrides = self.override
                limited = False
            else:
                displayed_overrides = self.override[:max_overrides]
                limited = True
            
            for exc in displayed_overrides:
                print("- {0}".format(exc))
            
            if limited:
                print("- ... ({0} more)".format(len(self.override)-max_overrides))
    
    def registry_read(self):
        """Read values from registry"""
        proxykey = winreg.OpenKey(_ROOT, _BASEKEY, 0, _ACCESS)
        self._enable = winreg.QueryValueEx(proxykey, _PROXYENABLE)
        self._http11 = winreg.QueryValueEx(proxykey, _PROXYHTTP11)
        self._server = winreg.QueryValueEx(proxykey, _PROXYSERVER)
        self._override = winreg.QueryValueEx(proxykey, _PROXYOVERRIDE)
        winreg.CloseKey(proxykey)
    
    def registry_write(self):
        """Write values to registry"""
        proxykey = winreg.OpenKey(_ROOT, _BASEKEY, 0, _ACCESS)
        value, regtype = self._enable
        winreg.SetValueEx(proxykey, _PROXYENABLE, 0, regtype, value)
        value, regtype = self._http11
        winreg.SetValueEx(proxykey, _PROXYHTTP11, 0, regtype, value)
        value, regtype = self._server
        winreg.SetValueEx(proxykey, _PROXYSERVER, 0, regtype, value)
        value, regtype = self._override
        winreg.SetValueEx(proxykey, _PROXYOVERRIDE, 0, regtype, value)
        winreg.CloseKey(proxykey)

    @property
    def enable(self):
        """Proxy enable status"""
        return self._enable[0] == 1
    
    @enable.setter
    def enable(self, on):
        """Set enable value from a boolean value"""
        if on:
            self._enable = (1, 4)
        else:
            self._enable = (0, 4)
    
    @property
    def http11(self):
        """Proxy http1.1 status"""
        return self._http11[0] == 1
    
    @http11.setter
    def http11(self, on):
        if on:
            self._http11 = (1, 4)
        else:
            self._http11 = (0, 4)
    
    @property
    def server(self):
        """Return the proxy server or proxy servers.
        
        If individual proxy servers are set, then return a dictionary
        mapping protocol to proxy:port, e.g.:
        
        dict(http='192.168.0.1:8000',
             https='192.168.0.1:8001')
        
        If only one proxy is used for all protocols, then return a
        dictionary of the form:
        
        dict(all='192.168.0.1:8000')
        
        If the proxy is disabled the property is None."""
        if not self.enable:
            return None
        # If protocol specific proxy settings are user, these are
        # assigned to the protocol names with the '=' sign
        if self._server[0].find('=') >= 0:
            servers = self._server[0].split(';')
            servers = dict(map(lambda p: p.split('='), servers))
        else:
            servers = dict(all=self._server[0])
        return servers
    
    @property
    def override(self):
        """Return a list of all proxy exceptions"""
        return self._override[0].split(';')
    
    @override.setter
    def override(self, overridelist):
        """Set the override value from a list of proxy exceptions"""
        self._override = (';'.join(overridelist), self._override[1])

