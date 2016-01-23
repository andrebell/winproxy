---
layout: default
---

# A Proxy Selection Tool for Windows

From time to time it is necessary to change the systems proxy settings. This
can be due to network changes or to test software with internet access on
different proxies or proxy settings. However, always walking through the
Windows system dialog and manually changing the settings is a tedious task.

Therefore, this small python project enables the quick change of the proxy
settings either programmatically by using the provided module functions, or
from the command line, by calling the command line scripts, that are part of
this project as well.

## The Command Line Tool

The proxy settings in Windows are basically given by four values:

  - ProxyEnable
  - ProxyHttp11
  - ProxyServer
  - ProxyOverride

If ProxyEnable is set to 0 no proxy will be used and if it is set to 1 the proxy
settings specified by the other values are in use.

Every value can be set individually or in combination with the "winproxy set"
command. E.g., to set the server value specifically for http you can call

```bash
C:\> winproxy set --http proxyserver:port
```

Setting a proxy server for all protocols to 10.0.0.1 on port 8080 except for the
local network and enable the proxy is achieved by

```bash
C:\> winproxy set -e 1 --all 10.0.0.1:8080 -o 10.*.*.*
```

Since turning the proxy on and off is quite common, the command line utility 
provides two convinience calls to turn the proxy on and off.

To turn the proxy on you have to call

```bash
C:\> winproxy on
```

from the command prompt and to turn the proxy off you have to run

```bash
C:\> winproxy off
```

respectively. You may want to display the current proxy settings by

```bash
C:\> winproxy view
```

If you do have man proxy exceptions (overrides), you can limit the number of
proxy exceptions displayed with the -n option:

```bash
C:\> winproxy view -n 5    # Display only the first 5 exceptions
```

```bash
C:\> winproxy view -n 0    # Don't display proxy exceptions at all
```

The full documentation of the command line interface will be given in the
documentation [TODO: Add Doc and link]

## The Python API

The python API for accessing and changing the proxy settings in windows is
build around a class called ProxySetting. By default, every new object of this
class is initialized with empty default values.

```python
>>> from winproxy import ProxySetting
>>> p = ProxySetting()
>>> p.display()
ProxyEnable: False
ProxyHttp11: True
ProxyServer: 
ProxyOverride:
```

To load the current proxy settings from the registry you can use the method
registry_read().

```python
>>> p.registry_read()
>>> p.display()
ProxyEnable: True
ProxyHttp11: True
ProxyServer: 10.0.0.1:8080
ProxyOverride: 
- <local>
```

You may change the settings using the properties enable, http11, server, and
override, which can directly be set with a bool, bool, string or dictionary, 
and a list respectively.

To give an example, setting the proxy server to new settings for http and
https, one could write

```python
>>> p.server = dict(http='10.0.0.1:8080', https='10.0.0.1:8081')
>>> p.display()
ProxyEnable: True
ProxyHttp11: True
ProxyServer: http=10.0.0.1:8080;https=10.0.0.1:8081
ProxyOverride:
- <local>
```

Writing the settings to the registry is achieved with the method registry_write.

```python
>>> p.registry_write()
```

The full documentation of the command line interface will be given in the
documentation [TODO: Add Doc and link]

## Change Log

### 0.4.0a1

* Changed winproxy set command line behaviour to only write those values to the
  registry, that have been provided as parameter and leave all others as is.
  This is way more flexible to use.
* Added some short, tutorial-like documentation for the command line.

### 0.3.0a1

* Added a first draft of the set command
* The winproxy view command was broken if
  * no overrides were set at all
  * less overrides were set, than should be shown at most
* The override list may contain not only ';' separated proxies, but also ','
  separated ones. This may even be mixed. Also, there may be whitespace in the
  Text. This all is now corrected for, i.e., setting override through the
  ProxySettings API will always normalize the string to ';' delimited proxies.
* Missing registry values fall back to sensible defaults

### 0.2.0a1

* Added the "winproxy cpl" to the command line to open the Windows Internet
  Settings dialog
* Added a change log to the README

### 0.1.0a1

* Basic ProxySettings class for the Python API
* Command line with "winproxy on|off|view" to
  * turn the proxy on
  * turn the proxy off
  * display the current proxy settings

## Authors

Andre Alexander Bell <winproxy@andre-bell.de>