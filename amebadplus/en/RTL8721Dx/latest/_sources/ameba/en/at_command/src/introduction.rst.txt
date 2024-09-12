.. _at_command:

Introduction
=============

This article describes the role, usage, version information, of AT command.
Users can perform some basic IoT applications, such as Wi-Fi, Bluetooth, TCP/IP, MQTT and other operations, with AT command.


We set the module as the slave, and the PC as the master. The master can send AT commands to the slave.
While receiving the AT command, the slave recognizes the validity of the command. If it is a valid command, it returns the corresponding AT response.

Overview
----------------
Regarding the different chips in slave module, we commonly call them AmebaLite, AmebaGreen2, AmebaSmart, and AmebaDPlus.
For their usages, the hardware connections are generally similar, but the interfaces used are slightly different.

There are two currently used AT command input and response methods, which can be called LOGUART mode and UART mode.

- In LOGUART mode, the log of the program is in the same window with the input and response of the AT command, but the connection of the device is relatively simple, the module can be directly connected to the PC by USB cable.

- In UART mode, the log of program, input and response of AT commands, are presented in their respective windows, so that the results of AT commands can be displayed to the user more clearly, which can facilitate some automated testing.

However, the device connection is relatively complicated, it requires an additional designated UART port to be connected to the PC through USB2TTL cable.


You can run ``make menuconfig`` to choose UART mode or LOGUART mode. The procedure is as follows:

.. code-block::

   // Your SDK direction
   cd $<sdk>
   // The chip type you choose, e.g. amebasmart
   cd source/<ameba_type>
   make menuconfig
   // ...

.. figure:: ../figures/general_config.png
   :scale: 60%
   :align: center
   :name: general_config

   Mode selection

Some hardwares are inquired at first.

- Ameba board: As a slave module.

- PC (or other master device): Download image, input AT commands, observe the response of AT commands.

- USB cables of type-C: Connect module to PC (or other master device).

- Several dupont lines: Connect module to USB2TTL in case of UART mode.

- USB2TTL: Used in case of UART mode, convert the USB signal into TTL signal, or vice versa.


In case of LOGUART mode, the input and response of AT commands are shown in the same port.

.. figure:: ../figures/loguart_mode.svg
   :scale: 90%
   :align: center

   LOGUART mode


In case of UART mode, the input and response of AT commands can be separated from the debug log, through the UART port, making it easier for users to view the execution results of AT commands more intuitively.

.. figure:: ../figures/uart_mode.svg
   :scale: 90%
   :align: center

   UART mode

For different ICs, the default UART input and output ports are listed below.

.. table:: Default UART port and baud rates for chips
   :width: 100%
   :widths: auto

   +-------------+---------+---------+-------------------+
   | IC          | UART TX | UART RX | Default baud rate |
   +=============+=========+=========+===================+
   | AmebaSmart  | PA 3    | PA_2    | 38400             |
   +-------------+---------+---------+-------------------+
   | AmebaLite   | PA_28   | PA_29   | 38400             |
   +-------------+---------+---------+-------------------+
   | AmebaDPlus  | PA_26   | PA_27   | 38400             |
   +-------------+---------+---------+-------------------+
   | AmebaGreen2 | PA_4    | PA_5    | 38400             |
   +-------------+---------+---------+-------------------+


You can modify these values in :file:`{sdk}/source/component/at_cmd/at_intf_uart.h`.

1. Modify the baud rate

.. code-block:: c

   #define UART_BAUD   38400

2. Modify the UART ports for chips

.. code-block:: c

   #if defined (CONFIG_AMEBASMART)
   #define UART_TX     _PA_3 // UART0 TX
   #define UART_RX     _PA_2 // UART0 RX
   #elif defined (CONFIG_AMEBALITE)
   #define UART_TX     _PA_28 // UART TX
   #define UART_RX     _PA_29 // UART RX
   #elif defined (CONFIG_AMEBADPLUS)
   #define UART_TX     _PA_26 // UART TX
   #define UART_RX     _PA_27 // UART RX
   #elif defined (CONFIG_AMEBAGREEN2)
   #define UART_TX     _PA_4 // UART TX
   #define UART_RX     _PA_5 // UART RX
   #endif


Command Description
--------------------------------------
Command Format
~~~~~~~~~~~~~~

The current format of the supported AT command set starts with two capital letters ``AT`` (abbreviation of attention), called the start characters, followed by a ``+``, then by the command name.
If there are several parameters more, it will be followed by an ``=``, then by a parameter list. For example:

.. code-block::

   AT+COMMAND=parameter1, parameter2

In this case, the first two letters ``AT`` are the start characters, indicating that the current string can be recognized as AT command, and ``+`` is used to separate the start characters and subsequent commands.
``COMMAND`` is the specific command name, to be executed right now. 
This command requires some parameters. It contains two parameters in this example: *parameter1* and *parameter2*. After entering this AT command, continue to press Enter (means newline) to start executing this AT command.


After receiving the AT command, the slave judges whether it is a valid command at first.
If it is considered as an invalid command (not in the AT command set), nothing will be performed.
Otherwise, it will be executed based on the input command and its parameters, if present.
When the command is successfully executed, the command name plus an **OK** mark will generally be returned.
When the command execution fails, the command name plus an **ERROR** mark will generally be returned, followed by an error code.


As in the above example, after the command executed, you can observe the result on the host side. If you see **OK** returned, it means the command has been executed successfully.
therwise, **ERROR** is returned, based on the subsequent error code, you can inquiry the error code corresponding to each command to find out what it means.


Sometimes, several parameters in AT command may be ignored, in this case, one or more comma(s) should be input inside parameters.

For example:

.. code-block::

   AT+COMMAND=parameter1, , parameter3

In this command above, there is an invisible *parameter2* between two commas, in this case, the *parameter2* is considered as a null string whose length equals to zero byte.
In this text, when introducing the parameter list of a certain AT command, angle brackets ``< >`` are added to indicate the name of the parameter, and square brackets ``[ ]`` are added to indicate that the parameter is optional.
Different parameters are separated by commas.

For example:

.. code-block::

   AT+COMMAND=<param1>[,<param2>,<param3>]

In this command, the 1st parameter named *param1* is mandatory, the 2nd parameter named *param2*, and the 3rd parameter named *param3* are optional.

Escapes Character
~~~~~~~~~~~~~~~~~~
Especially, in several AT commands, if you really need let one or more comma(s) be part(s) of a parameter, it is recommended to use escapes character ``\`` instead.
Furthermore, the backslash itself is expressed in escapes character ``\\``.


For example:

.. code-block::

   AT+COMMAND=parameter1,head\,tail,head\\tail

In this command, there are 3 parameters at all, the 2nd parameter is a string *head,tail* which includes a comma.
In this case, the comma inside *head,tail* will not be considered as a segmentation of parameters, but as a part of string.
And, the 3rd parameter is a string *head\\tail* including a backslash. Single backslash is illegal here, in other words, single backslash must be followed by a comma or another backslash in these AT commands.
For the other AT commands which do not need use escapes character, the comma will always be considered as a segmentation, and single backslash is allowed as a common character.


.. table:: Commands with escapes character
   :width: 100%
   :widths: auto

   +--------------+-------------------------------------+
   | AT command   | Parameter(s) with escapes character |
   +==============+=====================================+
   | AT+MQTTSUB   | <topic>                             |
   +--------------+-------------------------------------+
   | AT+MQTTUNSUB | <topic>                             |
   +--------------+-------------------------------------+
   | AT+MQTTPUB   | <topic>,<msg>                       |
   +--------------+-------------------------------------+
   | AT+SKTSEND   | <data>                              |
   +--------------+-------------------------------------+

Command Length
~~~~~~~~~~~~~~~

Each AT command must not exceed a length limit, otherwise, the excess part will be ignored.

There are 2 types of length limit. When longer command format is enabled, the length limit is 511 bytes, otherwise (shorter command format), the length limit is 126 bytes.
When the AT command using escapes character, the escapes characters such as '``\`` or ``\\`` should be regarded as 2 bytes.
Especially, the longer command format is not available for AmebaGreen2 yet.

You can modify the length limit by ``make menuconfig`` when compiling the SDK. If you select the option ``Enable Longer CMD``, the length limit will be larger.

AT Command List
------------------------------
The AT commands supported now are listed in the following table.

.. table:: AT commands list
   :width: 100%
   :widths: auto

   +------------------------------------------------------+--------------------------------------------------------------+-----------------------------------------------------------+
   | Type                                                 | AT Command                                                   | Description                                               |
   +======================================================+==============================================================+===========================================================+
   | :ref:`Common AT Commands<common_at_commands>`        | :ref:`AT+TEST<common_at_test>`                               | Test AT command ready                                     |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+LIST<common_at_list>`                               | Print all AT commands                                     |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+OTACLEAR<common_at_otaclear>`                       | Clear the APP image OTA2 signature                        |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+OTARECOVER<common_at_otarecover>`                   | Recover the APP image OTA2 signature                      |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+CPULOAD<common_at_cpuload>`                         | Get the CPU load periodically                             |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+RST<common_at_rst>`                                 | Restart the module                                        |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+STATE<common_at_state>`                             | List all running tasks, and current heap                  |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+GMR<common_at_gmr>`                                 | Show the release version and date                         |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+LOG<common_at_log>`                                 | Get set or clear the log level                            |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+RREG<common_at_rreg>`                               | Read the common register value                            |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WREG<common_at_wreg>`                               | Write data into register                                  |
   +------------------------------------------------------+--------------------------------------------------------------+-----------------------------------------------------------+
   | :ref:`Wi-Fi AT Commands<wi_fi_at_commands>`          | :ref:`AT+WLCONN<wi_fi_at_wlconn>`                            | Connect to AP (STA mode)                                  |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLDISCONN<wi_fi_at_wldisconn>`                      | Disconnect from AP                                        |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLSTATICIP<wi_fi_at_wlstaticip>`                    | Set static IP for station                                 |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+PING<wi_fi_at_ping>`                                | PING a domain or IP address                               |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+IPERF<wi_fi_at_iperf>`                              | IPERF test for TCP or UDP                                 |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+IPERF3<wi_fi_at_iperf3>`                            | IPERF3 test for TCP                                       |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLSCAN<wi_fi_at_wlscan>`                            | Scan the Wi-Fi                                            |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLRSSI<wi_fi_at_wlrssi>`                            | Get the RSSI of connected AP currently                    |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLSTARTAP<wi_fi_at_wlstartap>`                      | Start this module as a Wi-Fi AP                           |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLSTOPAP<wi_fi_at_wlstopap>`                        | Stop this module as a Wi-Fi AP                            |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLSTATE<wi_fi_at_wlstate>`                          | Get the Wi-Fi state of module, maybe as an AP or a device |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLRECONN<wi_fi_at_wlreconn>`                        | Enable or disable Wi-Fi auto-connection                   |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLPROMISC<wi_fi_at_wlpromisc>`                      | Enable or disable Wi-Fi promisc                           |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLDBG<wi_fi_at_wldbg>`                              | Test Wi-Fi iwpriv command                                 |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLWPS<wi_fi_at_wlwps>`                              | Test Wi-Fi wps command                                    |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+WLPS<wi_fi_at_wlps>`                                | Enable or disable lps, ips                                |
   +------------------------------------------------------+--------------------------------------------------------------+-----------------------------------------------------------+
   | :ref:`MQTT AT Commands<mqtt_at_commands>`            | :ref:`AT+MQTTOPEN<mqtt_at_mqttopen>`                         | Create an MQTT entity                                     |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+MQTTCLOSE<mqtt_at_mqttclose>`                       | Delete an MQTT entity                                     |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+MQTTCONN<mqtt_at_mqttconn>`                         | Connect to host server                                    |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+MQTTDISCONN<mqtt_at_mqttdisconn>`                   | Disconnect from host server                               |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+MQTTSUB<mqtt_at_mqttsub>`                           | Subscribe a topic from host server                        |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+MQTTUNSUB<mqtt_at_mqttunsub>`                       | Unsubscribe a topic from host server                      |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+MQTTPUB<mqtt_at_mqttpub>`                           | Publish a message for specific topic                      |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+MQTTCFG<mqtt_at_mqttcfg>`                           | Configure the parameters of MQTT entity                   |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+MQTTRESET<mqtt_at_mqttreset>`                       | Reset all MQTT entities                                   |
   +------------------------------------------------------+--------------------------------------------------------------+-----------------------------------------------------------+
   | :ref:`TCP/IP AT Commands<tcp_ip_at_commands>`        | :ref:`AT+SKTSERVER<tcp_ip_at_sktserver>`                     | Start as a socket server                                  |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+SKTCLIENT<tcp_ip_at_sktclient>`                     | Start as a socket client                                  |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+SKTDEL<tcp_ip_at_sktdel>`                           | Stop a (all) socket server(s) or client(s)                |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+SKTTT<tcp_ip_at_skttt>`                             | Enable transparent transfer mode                          |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+SKTSEND<tcp_ip_at_sktsend>`                         | Send socket message                                       |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+SKTREAD<tcp_ip_at_sktread>`                         | Receive socket message                                    |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+SKTRECVCFG<tcp_ip_at_sktrecvcfg>`                   | Configure socket receiving                                |
   |                                                      +--------------------------------------------------------------+-----------------------------------------------------------+
   |                                                      | :ref:`AT+SKTSTATE<tcp_ip_at_sktstate>`                       | Get the socket state currently                            |
   +------------------------------------------------------+--------------------------------------------------------------+-----------------------------------------------------------+
   | :ref:`Bluetooth AT Commands<bluetooth_at_commands>`  |                                                              |                                                           |
   +------------------------------------------------------+--------------------------------------------------------------+-----------------------------------------------------------+


Building Image
----------------------
Preparation
~~~~~~~~~~~~~~~~~~~~~~
Users can also build images with ``{sdk}`` by self. For detailed building procedure, please refer to the AN documents for different type of chips.

Building
~~~~~~~~~~~~~~~~
After preparations above, user can build images in the ``{sdk}`` directory.

.. code-block::

   cd ${sdk}
   // The <ameba_type> is different for chips
   cd source/<ameba_type>
   // make menuconfig is optional, if you need modify some options
   make menuconfig
   make all

If somehow failed, type ``$make clean`` to clean, then redo the make procedure.

After building successfully, the image files can be found at ``{ameba_type}`` directory.

Downloading Image
----------------------------
There are two ways to download image to Flash:

(1) Image Tool, a software provided by Realtek (recommended).

(2) GDB Server, mainly used for GDB debug user case.

In this section, we will introduce the first one.

The Image Tool is the official image download tool developed by Realtek for Ameba series SoC. It can be used to download images to the Flash of device through the UART download interface.

When you open the image tool, it is shown as the following figure.

.. figure:: ../figures/Download_image.png
   :scale: 70%
   :align: center

   Image Tool

Device profiles provide the necessary device information required for image download, with the naming rules:

.. code-block::

   <SoC name>_<OS type>_<Flash type>[_<Extra info>].rdev

For different type of chips, you should select the corresponding rdev file before downloading image to flash. You can click the :menuselection:`File > Open` to select corresponding rdev file. Then, select the corresponding image files.

Bofore downloading image, the chip should enter download mode at first.
You can press and hold the :guilabel:`DOWNLOAD` button on chip, then press the :guilabel:`CHIP_EN` button, the chip will enter download mode after you loosen them both.

Then connect the chip module to PC with USB cable, and press the :guilabel:`DOWNLOAD` button of Image Tool to start downloading the image files.



