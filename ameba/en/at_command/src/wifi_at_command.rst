.. _wi_fi_at_commands:

Wi-Fi AT Commands
==================================

.. _wi_fi_at_wlconn:

AT+WLCONN
------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Connect to AP (STA mode).

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLCONN=[<type>,<value>,<type>,<value>,……]

Response
~~~~~~~~~~~~~~~~
.. code::

   +WLCONN:OK

Or

.. code::

   +WLCONN:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<type>: The type of the followed parameter <value>.

   - "ssid": The <ssid> should be followed.

   - "bssid": The <bssid> should be followed.

   - "ch": The <ch> should be followed.

   - "pw": The <pw> should be followed.

   - "key_id": The <key_id> should be followed.

<value>: The parameter followed correspond <type>, as bellow:

<ssid>: The ssid of Wi-Fi.

   - A name string with length shorter than 33.

<bssid>: The bssid of Wi-Fi.

   - A hexadecimal number string separated by colons, such as 1a:2b:3c:4d:5e:6f.

<pw>: The password of Wi-Fi.

<key_id>: Key id of Wi-Fi.

   - [0,3].

<ch>: Channel of Wi-Fi.

   - The channel of Wi-Fi. It is 0 as default if this parameter is absent.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Error parameter number.

- 2: Error parameter.

- 3: Memory failure.

- 4: Can not connect to this Wi-Fi.

- 5: Wi-Fi is not on.

Example
~~~~~~~~~~~~~~
.. code::

   // Connect to a Wi-Fi with ssid and password
   AT+WLCONN=ssid,ssid_name,pw,12345678
   +WLCONN:OK
   // Connect to a Wi-Fi with ssid, password, key
   AT+WLCONN=ssid,ssid_name,key_id,1,pw,12345678
   +WLCONN:OK
   // Connect Wi-Fi with BSSID
   AT+WLCONN=bssid,1a:2b:3c:4d:5e:6f,pw,12345678
   +WLCONN:OK

.. _wi_fi_at_wldisconn:

AT+WLDISCONN
------------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Disconnect from AP.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLDISCONN

Response
~~~~~~~~~~~~~~~~
.. code::

   +WLDISCONN:OK

Or

.. code::

   +WLDISCONN:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
NULL

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 3: API error when disconnecting.

- 4: Timeout.

.. _wi_fi_at_wlstaticip:

AT+WLSTATICIP
--------------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Set static IP for station.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLSTATICIP=<ip>[,<gateway>,<netmask>]

Response
~~~~~~~~~~~~~~~~
.. code::

   +WLSTATICIP:OK

Or

.. code::

   +WLSTATICIP:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<ip>: IP address.

   - A data string of IP address, e.g. 192.168.10.33.

<gateway>: Gateway of station.

   - A data string of gateway, e.g. 192.168.10.1.

<netmask>: Netmask of station.

   - A data string of netmask, e.g. 255.255.255.0.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 3: API error when disconnecting.

- 4: Timeout.

.. _wi_fi_at_ping:

AT+PING
--------------
Description
~~~~~~~~~~~~~~~~~~~~~~
PING a domain or IP address.

Command
~~~~~~~~~~~~~~
.. code::

   AT+PING=<host>[<-t>,<interval>,<-n>,<count>,<-l>,<size>]
   AT+PING=<stop>

Response
~~~~~~~~~~~~~~~~
.. code::

   +PING:OK

Or

.. code::

   +PING:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<host>: The address of host.

   - An IP address, or dns address.

<-t>: It will followed by <interval>.

<interval>: Interval time in second.

   - A positive number.

   - If <-t> <interval> are absent, it is 1s as default.

<-n>: It will followed by <count>.

<count>: Ping packets number.

   - A positive number.

   - If <-n> <count> are absent, it is 4 as default.

<-l>: It will followed by <size>.

<size>: Ping packet size in byte.

   - A positive number.

   - If <-l> <size> are absent, it is 32 bytes as default.

<stop>: Stop the ongoing ping procedure.

   - "stop": It will stop the ongoing ping procedure.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Input null parameter.

- 2: Error parameter number.

Note
~~~~~~~~
.. note::
   In this command, the sequence of <-t> <-l> <-n> is not required.

   The response of each packet can be only observed at log window.

   The response "OK" means this command's format is correct, but not ping the target successfully.


Example
~~~~~~~~~~~~~~
.. code::

   // Default parameters
   AT+PING=192.168.31.200
   [ping_test] 32 bytes from 192.168.31.1: icmp_seq=1 time=135 ms
   [ping_test] 32 bytes from 192.168.31.1: icmp_seq=2 time=5 ms
   [ping_test] 32 bytes from 192.168.31.1: icmp_seq=3 time=102 ms
   [ping_test] 32 bytes from 192.168.31.1: icmp_seq=4 time=3 ms
   [ping_test] 4 packets transmitted, 4 received, 0% packet loss, average 60 ms
   [ping_test] min: 3 ms, max: 135 ms
   +PING:OK
   // Ping a web address for 3 times, with packet of 128 bytes
   AT+PING=www.sohu.com,-n,3,-l,128
   [ping_test] 128 bytes from 192.168.31.1: icmp_seq=1 time=40 ms
   [ping_test] 128 bytes from 192.168.31.1: icmp_seq=2 time=9 ms
   [ping_test] 128 bytes from 192.168.31.1: icmp_seq=3 time=21 ms
   [ping_test] 3 packets transmitted, 3 received, 0% packet loss, average 23 ms
   [ping_test] min: 9 ms, max: 40 ms
   +PING:OK

.. _wi_fi_at_iperf:

AT+IPERF
----------------
Description
~~~~~~~~~~~~~~~~~~~~~~
IPERF test for TCP or UDP.

Command
~~~~~~~~~~~~~~
.. code::

   AT+IPERF=<-s>[,<-p>,<port>,<-u>]

Or

.. code::

   AT+IPERF=<-c>,<host|stop>[,<-i>,<periodic>,<-l>,<size>,<-u>,<-b>,<bandwidth>,<-d>,<-t>,<transtime>,<-n>,<count>,<-S>]

Response
~~~~~~~~~~~~~~~~
.. code::

   +IPERF:OK

Or

.. code::

   +IPERF:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<-s>: Work as a server.

<-c>: Work as a client.

<-p>: It will be followed by <port>.

<port>: The server port.

   - [1,65535].

   - It is 5001 as default if absent.

<-u>: Work in UDP.

   - If absent, it works in TCP as default.

<host|stop>: A host name or stop stream id.

   - <stop>: Terminate specific stream id or terminate all stream if no id.

   - <host>: The host name of service.

<-i>: It will be followed by <periodic>.

<periodic>: Seconds between periodic bandwidth reports.

   - A positive number.

<-l>: It will be followed by <size>.

<size>: Packet size to read or write.

   - A positive number.

   - It is 1460 bytes as default if absent.

<-b>: It will be followed by <bandwidth>.

<bandwidth>: For UDP, the bandwidth in bits/sec.

   - If <-b>, <bandwidth> are absent, it is 1 bits/sec as default.

<-d>: Do a bidirectional test simultaneously.

<-t>: It will be followed by <transtime>.

<transtime>: Time in seconds to transmit for.

   - If <-t>, <transtime> are absent, it is 10 seconds as default.

<-n>: It will be followed by <count>.

<count>: Number of bytes to transmit.

   - A positive number.

<-S>: For UDP, set the IP "type of service".

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Input null parameter.

- 3: Error parameter number.

Note
~~~~~~~~
.. note::
   In this command, the sequence of <-t> <-l> <-n>, etc. is not required.


Example
~~~~~~~~~~~~~~
.. code::

   // For TCP
   AT+IPERF=-s,-p,5002
   +IPERF:OK
   AT+IPERF=-c,192.168.1.2,-t,100,-p,5002
   +IPERF:OK
   // For UDP
   AT+IPERF=-c,192.168.1.2,-t,100,-p,5002,-u
   +IPERF:OK

.. _wi_fi_at_iperf3:

AT+IPERF3
------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
IPERF3 test for TCP.

Command
~~~~~~~~~~~~~~
.. code::

   AT+IPERF3=<-s>[<-p>,<port>]

Or

.. code::

   AT+IPERF3=<-c>,<host|stop>[,<-i>,<periodic>,<-l>,<size>,<-d>,<-t>,<transtime>,<-n>,<count>]

Response
~~~~~~~~~~~~~~~~
.. code::

   +IPERF3:OK

Or

.. code::

   +IPERF3:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<-s>: Work as a server.

<-c>: Work as a client.

<-p>: It will be followed by <port>.

<port>: The server port.

   - [1,65535].

   - It is 5001 as default if absent.

<host|stop>: A host name or stop stream id.

   - <stop>: Terminate specific stream id or terminate all stream if no id.

   - <host>: The host name of service.

<-i>: It will be followed by <periodic>.

<periodic>: Seconds between periodic bandwidth reports.

   - A positive number.

<-l>: It will be followed by <size>.

<size>: Packet size to read or write.

   - A positive number.

   - It is 1460 bytes as default if absent.

<-d>: Do a bidirectional test simultaneously.

<-t>: It will be followed by <transtime>.

<transtime>: Time in seconds to transmit for.

   - If <-t>, <transtime> are absent, it is 10 seconds as default.

<-n>: It will be followed by <count>.

<count>: Number of bytes to transmit.

   - A positive number.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Input null parameter.

- 2: Error parameter number.

Note
~~~~~~~~
.. note::
   In this command, the sequence of <-t> <-l> <-n>, etc. is not required.


Example
~~~~~~~~~~~~~~
.. code::

   AT+IPERF3=-s,-p,5002
   AT+IPERF3=-c,192.168.1.2,-t,100,-p,5002

.. _wi_fi_at_wlscan:

AT+WLSCAN
------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Scan the Wi-Fi.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLSCAN

Or

.. code::

   AT+WLSCAN=[<type>,<value>,<type>,<value>]

Response
~~~~~~~~~~~~~~~~
.. code::

   // The first Wi-Fi scanned
   <bss_type>  <mac>  <rssi>  <channel>  <wps>  <security>  <aes>  <ssid>
   // Any other Wi-Fi if exists
   // ……
   +WLSCAN:OK

Or

.. code::

   +WLSCAN:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<type>: The parameter's type.

   - "ssid": It is followed by <ssid>.

   - "ch": It is followed by <chlist>.

<value>: The parameter followed <type>.

   - <ssid>: the string of ssid name.

   - <chlist>: The channel list, segmented by colons.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Error Wi-Fi join status.

- 3: Memory failure.

- 5: Failed when scanning.

Note
~~~~~~~~
.. note::
   The sequence beyond different <type>s is not inquired.


Example
~~~~~~~~~~~~~~
.. code::

   // Scan 2 channels, 1 and 2.
   AT+WLSCAN=ch,1:2
   +WLSCAN:OK
   1   Infra   64:64:4a:86:a6:8e, -51    1     7    WPA/WPA2 Mixed      Xiaomi_F4D4
   2   Infra   68:dd:b7:6b:84:ba, -54    1     6    WPA/WPA2 AES      MatCH
   3   Infra   1c:fa:68:f8:c4:9c, -60    1     7    WPA/WPA2 AES      ATS_Linux_2.4G
   4   Infra   d4:ee:07:61:d0:c2, -61    1     6    WPA/WPA2 AES      HiWiFi_61D0C2
   // Scan ssid
   AT+WLSCAN=ssid,TP-LINK_BCC7
   +WLSCAN:OK
   1   Infra   7c:b5:9b:c3:bc:c7, -65    4     6    WPA/WPA2 AES      TP-LINK_BCC7
   // Scan both ssid and channels (1 to 6)
   AT+WLSCAN=ssid,Xiaomi_F4D4,ch,1:2:3:4:5:6
   +WLSCAN:OK
   1   Infra   64:64:4a:86:a6:8e, -54    1     7    WPA/WPA2 Mixed      Xiaomi_F4D4

.. _wi_fi_at_wlrssi:

AT+WLRSSI
------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Get the RSSI of connected AP currently.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLRSSI

Response
~~~~~~~~~~~~~~~~
.. code::

   rssi = <rssi>
   data rssi = <data_rssi>
   beacon rssi = <beacon_rssi>
   +WLRSSI:OK

Parameter
~~~~~~~~~~~~~~~~~~
NULL

Note
~~~~~~~~
.. note::
   If it is not connected status right now, there will be still a response output, but it is meaningless.

.. _wi_fi_at_wlstartap:

AT+WLSTARTAP
------------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Start this module as a Wi-Fi AP.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLSTARTAP=[<type>,<value>,<type>,<value>,……]

Response
~~~~~~~~~~~~~~~~
.. code::

   +WLSTARTAP:OK

Or

.. code::

   +WLSTARTAP:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<type>: The type of the followed parameter <value>.

   - "ssid": The <ssid> should be followed.

   - "ch": The <ch> should be followed.

   - "pw": The <pw> should be followed.

   - "sec ": The <sec> should be followed.

<value>: The parameter followed correspond <type>, as bellow:

<ssid>: The string of ssid name.

<ch>: Channel of AP.

   - [1,11].

<sec>: The security type, with string format.

   - "open".

   - "wep".

   - "tpic".

   - "wpa2".

   - "wpa3".

<pw>: The string of password.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Input null parameter.

- 2: Error parameter.

- 3: Timeout.

- 4: Failed when starting AP.

- 5: Memory failure.

Example
~~~~~~~~~~~~~~
.. code::

   // Start with anonymous Wi-Fi
   AT+WLSTARTAP=ssid,new_ssid,ch,1,sec,open
   +WLSTARTAP:OK
   // Start AP with wpa2 type
   AT+WLSTARTAP=sec,wpa2,pw,12345678,ssid,new_ssid
   +WLSTARTAP:OK
   // Now you can connect new_ssid with mobile-phone, or another board

.. _wi_fi_at_wlstopap:

AT+WLSTOPAP
----------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Stop this module as a Wi-Fi AP.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLSTOPAP

Response
~~~~~~~~~~~~~~~~
.. code::

   +WLSTOPAP:OK

Parameter
~~~~~~~~~~~~~~~~~~
NULL

.. _wi_fi_at_wlstate:

AT+WLSTATE
--------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Get the Wi-Fi state of module, maybe as an AP or a device.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLSTATE

Response
~~~~~~~~~~~~~~~~
.. code::

   WLAN0 Status: <status>
   ==============================
   max_skbinfo_used_num=<maxinfonum>, skbinfo_used_num=<usedinfonum>
   max_skbdata_used_num=<maxdatanum>, skbdata_used_num=<useddatanum>
   // As an device, the information ……
   WLAN0 Setting:
   ==============================
   MODE => STATION
   SSID => <wifi_ssid> // If connected
   BSSID => <bssid> // If connected
   CHANNEL => <channel>
   SECURITY => <security>
   PASSWORD =>
   Interface (0)
   ==============================
   MAC => <mac_address>
   IP  => <ip_address>
   GW  => <gateway>
   msk  => <netmask>
   // As an AP, the information ……
   WLAN1 Status: <status>
   ==============================
   WLAN1 Setting:
   ==============================
   MODE => AP
   SSID => <ssid>
   BSSID => <bssid>
   CHANNEL => <channel>
   SECURITY => <security>
   PASSWORD =>
   Interface (1)
   ==============================
   MAC => <mac_address>
   IP  => <ip_address>
   GW  => <gateway>
   msk  => <netmask>
   Associated Client List:
   ==============================
   Client Num: <client_num>  // If exist
   Client 1:  // If exist
   MAC => <client_mac_address>
   // Any other clients if exist.
   +WLSTATE:OK

.. _wi_fi_at_wlreconn:

AT+WLRECONN
--------------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Enable or disable Wi-Fi auto-connection.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLRECONN=<command>,<parameter>

Response
~~~~~~~~~~~~~~~~
.. code::

   +WLRECONN:OK

Or

.. code::

   +WLRECONN:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<command>: Set auto connect or fast re-connect.

   - "auto": auto reconnect when wifi disconnect or connect fail.

   - "fast": Fast reconnect when wifi power on.

<parameter>: The corresponding value for <command>.

   - 0: Disable auto-reconnect when <command> is auto. Clear stored flash when <command> is fast.

   - 1: Enable auto-reconnect when <command> is auto. Allow fast reconnect when <command> is fast.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Error parameter number.

- 2: Invalid <enable> value.

.. _wi_fi_at_wlpromisc:

AT+WLPROMISC
------------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Enable or disable Wi-Fi promisc.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLPROMISC=<enable>[,<all/apall>]

Response
~~~~~~~~~~~~~~~~
.. code::

   +WLPROMISC:OK

Or

.. code::

   +WLPROMISC:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<enable>: Enable or disable Wi-Fi promisc, with string format.

   - "enable": Enable.

   - "disable": Disable.

<all/apall>: Filter mode.

   - "all": All packets.

   - "apall": Only AP related packets.

   - If <enable> equals to "enable", the <all/apall> is mandatory.

Note
~~~~~~~~
.. note::
   The <all/apall> is only needed when <enable> equals to "enable".

.. _wi_fi_at_wldbg:

AT+WLDBG
----------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Test Wi-Fi iwpriv command.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLDBG=<command>[,<parameters>]

Response
~~~~~~~~~~~~~~~~
.. code::

   +WLDBG:OK

Or

.. code::

   +WLDBG:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<command>: The iwpriv command, with string format.

   - Including command and command length.

<parameters>: The parameters of specific command.

   - Including api_id, api_parameters for debugging.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Input error parameter.

- 2: Failed when do iwpriv testing.

.. _wi_fi_at_wlwps:

AT+WLWPS
----------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Test Wi-Fi wps command.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLWPS=<pcb_pin>[,<pin_val>]

Response
~~~~~~~~~~~~~~~~
.. code::

   +WLWPS:OK

Or

.. code::

   +WLWPS:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<pcb_pin>: The string of "pcb" or "pin".

   - "pcb": Start wps pcb.

   - "pin": Start wps pin display or keypad.

<pin_val>: The pin value.

   - The pin has a valid checksum.

   - If <pcb_pin> equals to "pin", the <pin_val> is mandatory.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Input error parameter.

Note
~~~~~~~~
.. note::
   The <pin_val> is only used when <pcb_pin> equals to "pin".

.. _wi_fi_at_wlps:

AT+WLPS
--------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Enable or disable lps, ips.

Command
~~~~~~~~~~~~~~
.. code::

   AT+WLPS=<mode>,<enable>[,<mode>,<enable>]

Response
~~~~~~~~~~~~~~~~
.. code::

   +WLPS:OK

Or

.. code::

   +WLPS:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<mode>: The string of "lps" or "ips".

   - "lps": LPS.

   - "ips": IPS.

<enable>: Enable or disable LPS/IPS.

   - 0: Disable.

   - 1: Enable.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Input error parameter number.

- 2: Error <lps_ips>.

Example
~~~~~~~~~~~~~~
.. code::

   AT+WLPS=lps,1
   +WLPS:OK
   AT+WLPS=ips,0
   +WLPS:OK
   AT+WLPS=lps,0,ips,1
   +WLPS:OK
