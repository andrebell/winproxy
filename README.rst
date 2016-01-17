A Proxy Selection Tool for Windows
==================================

From time to time it is necessary to change the systems proxy settings. This
can be due to network changes or to test software with internet access on
different proxies or proxy settings. However, always walking through the
Windows system dialog and manually changing the settings is a tedious task.

Therefore, this small python project enables the quick change of the proxy
settings either programmatically by using the provided module functions, or
from the command line, by calling the command line scripts, that are part of
this project as well.

The Command Line Tool
---------------------

[TODO: Description]

To turn on the proxy call

  > winproxy on

from the command prompt and to turn off the proxy run

  > winproxy off

from the command prompt. You may want to display the current proxy settings by

  > winproxy view

If you do have man proxy exceptions (overrides), you can limit the number of
proxy exceptions displayed with the -n option:

  > winproxy view -n 5    # Display only the first 5 exceptions

  > winproxy view -n 0    # Don't display proxy exceptions at all

The Python API
--------------

[TODO: API Description]

Change Log
----------

0.3.0a1
~~~~~~~

* Added a first draft of the set command
* The winproxy view command was broken if
  * no overrides were set at all
  * less overrides were set, than should be shown at most

0.2.0a1
~~~~~~~

* Added the "winproxy cpl" to the command line to open the Windows Internet
  Settings dialog
* Added a change log to the README

0.1.0a1
~~~~~~~

* Basic ProxySettings class for the Python API
* Command line with "winproxy on|off|view" to
  * turn the proxy on
  * turn the proxy off
  * display the current proxy settings

Authors
-------
Andre Alexander Bell <winproxy@andre-bell.de>
