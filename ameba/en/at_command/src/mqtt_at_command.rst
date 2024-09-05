.. _mqtt_at_commands:

MQTT AT Commands
================================

.. _mqtt_at_mqttopen:

AT+MQTTOPEN
----------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Create an MQTT entity.

Command
~~~~~~~~~~~~~~
.. code::

   AT+MQTTOPEN=<con_id>,<host>[,<port>]

Response
~~~~~~~~~~~~~~~~
.. code::

   +MQTTOPEN:OK

Or

.. code::

   +MQTTOPEN:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<con_id>: The connect entity id.

   - [0,3]

<host>: The string of host name.

   - Not longer than 490 bytes when longer command format, otherwise not longer than 97 bytes.

<port>: The connection port.

   - [1,65535]

   - It is 1883 as default if absent.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Common error in software.

- 2: Error parameters.

- 3: Already existed connect id.

- 4: Memory failure.

- 9: Invalid connect id.

- 18: Task failure.

- 19: Network is not connected yet.

Example
~~~~~~~~~~~~~~
.. code::

   // At first, you should connect a Wi-Fi
   AT+MQTTOPEN=1,my_test_host,1883
   +MQTTOPEN:OK

.. _mqtt_at_mqttclose:

AT+MQTTCLOSE
------------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Delete an MQTT entity.

Command
~~~~~~~~~~~~~~
.. code::

   AT+MQTTCLOSE=<con_id>

Response
~~~~~~~~~~~~~~~~
.. code::

   +MQTTCLOSE:OK

Or

.. code::

   +MQTTCLOSE:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<con_id>: The connect entity id.

   - [0,3]

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Common error in software.

- 2: Error parameters.

- 3: Already existed connect id.

- 4: Memory failure.

- 6: This connect id has not been created.

- 9: Invalid connect id.

- 11. Can not disconect.

Note
~~~~~~~~
.. note::
   If this MQTT entity has connected to the server, you'd better execute AT+MQTTDISCONN at first, then close this entity.

.. _mqtt_at_mqttconn:

AT+MQTTCONN
----------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Connect to host server.

Command
~~~~~~~~~~~~~~
.. code::

   AT+MQTTCONN=<con_id>,<clientid>[,<username>,<password>]

Response
~~~~~~~~~~~~~~~~
.. code::

   // Here, this OK will be response immediately, if the command is correct.
   +MQTTCONN:OK
   // Here, once received ACK from host, it will response right now.
   ACK

Or

.. code::

   +MQTTCONN:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<con_id>: The connect entity id.

   - [0,3]

<clientid>: The string of client id.

   - It has length not longer than 490 bytes when longer command format, otherwise not longer than 97 bytes.

<username>: The string of username.

   - It has length not longer than 490 bytes when longer command format, otherwise not longer than 97 bytes.

<password>: The string of pasword.

   - It has length not longer than 490 bytes when longer command format, otherwise not longer than 97 bytes.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Common error in software.

- 2: Error parameters.

- 5: Attach error.

- 6: This connect id has not been created.

- 7: Can not connect to host.

- 9: Invalid connect id.

- 17: Time out.

Example
~~~~~~~~~~~~~~
.. code::

   // Connect to a service with username and password
   AT+MQTTCONN=1,my_test_host,user_test,pswd_test
   +MQTTCONN:OK
   ACK
   // Connect to an anonymous service
   AT+MQTTCONN=1,my_anonymous_host
   +MQTTCONN:OK
   ACK

.. _mqtt_at_mqttdisconn:

AT+MQTTDISCONN
----------------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Disconnect from host server.

Command
~~~~~~~~~~~~~~
.. code::

   AT+MQTTDISCONN=<con_id>

Response
~~~~~~~~~~~~~~~~
.. code::

   +MQTTDISCONN:OK

Or

.. code::

   +MQTTDISCONN:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<con_id>: The connect entity id.

   - [0,3]

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Common error in software.

- 2: Error parameters.

- 6: This connect id has not been created.

- 9: Invalid connect id.

- 10: It is not connected before.

- 17: Time out.

.. _mqtt_at_mqttsub:

AT+MQTTSUB
--------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Subscribe a topic from host server.

Command
~~~~~~~~~~~~~~
.. code::

   AT+MQTTSUB=<con_id>,<topic_string>[,<qos>]

Response
~~~~~~~~~~~~~~~~
.. code::

   // Here, this response will be output immediately once the command is correct.
   +MQTTSUB:OK
   // Here, once received ACK from host, it will response here.
   ACK

Or

.. code::

   +MQTTSUB:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<con_id>: The connect entity id.

   - [0,3]

<topic_string>: The string of topic to be subscibed.

   - It has length not longer than 490 bytes when longer command format, otherwise not longer than 97 bytes.

<qos>: The QoS value.

   - [0,2]

   - It is 2 as default if absent.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Common error in software.

- 2: Error parameters.

- 6: This connect id has not been created.

- 9: Invalid connect id.

- 10: It is not connected before.

- 13: Can not subscribe this topic.

- 14: Has subscribed this topic already.

- 17: Time out.

.. _mqtt_at_mqttunsub:

AT+MQTTUNSUB
------------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Unsubscribe a topic from host server.

Command
~~~~~~~~~~~~~~
.. code::

   AT+MQTTUSSUB=<con_id>,<topic_string>

Response
~~~~~~~~~~~~~~~~
.. code::

   // Here, this response will be output immediately once the command is correct.
   +MQTTUNSUB:OK
   // Here, once received ACK from host, it will response here.
   ACK

Or

.. code::

   +MQTTUNSUB:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<con_id>: The connect entity id.

   - [0,3]

<topic_string>: The string of topic to be subscibed.

   - It has length not longer than 490 bytes when longer command format, otherwise not longer than 97 bytes.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Common error in software.

- 2: Error parameters.

- 6: This connect id has not been created.

- 9: Invalid connect id.

- 10: It is not connected before.

- 16: Can not unsubscribe this topic.

- 17: Time out.

.. _mqtt_at_mqttpub:

AT+MQTTPUB
--------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Publish a message for specific topic.

Command
~~~~~~~~~~~~~~
.. code::

   AT+MQTTPUB=<con_id>,<messageid>[,<qos>,<retain>],<topic>,<message>

Response
~~~~~~~~~~~~~~~~
.. code::

   // Here, this response will be output immediately once the command is correct.
   +MQTTPUB:OK
   // Here, there may be the message callback
   +MQTTRECV:<conn_id>,<messageid>,<topic>,<message>,<length>,<qos>,<dup>,<retain>
   // Here, once received ACK from host, it will response here.
   ACK

Or

.. code::

   +MQTTPUB:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<con_id>: The connect entity id.

   - [0,3]

<messageid>: The message id.

   - [1,65534]

<qos>: QoS value.

   - [0,2]

   - It is 2 as default if absent.

<retain>: Retain value.

   - [0,1]

   - It is 0 as default if absent.

<topic>: The string of topic.

   - It has length not longer than 490 bytes when longer command format, otherwise not longer than 97 bytes.

   - It is suggested to fill a topic subscribed before.

<msg_string>: The message you will send.

   - It has length not longer than 490 bytes when longer command format, otherwise not longer than 97 bytes.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Common error in software.

- 2: Error parameters.

- 4. Memory failure.

- 6: This connect id has not been created.

- 9: Invalid connect id.

- 10: It is not connected before.

- 12: Can not publish successfully.

- 17: Time out.

Note
~~~~~~~~
.. note::
   The <qos> and <retain> are optional.



Example
~~~~~~~~~~~~~~
.. code::

   // Normal message
   AT+MQTTPUB=1,1,2,0,topic_test,my_message
   +MQTTPUB:OK
   +MQTTRECV:1,1,topic_test,my_message,10,0,0,0
   ACK
   // Json message, with commas in message, and ignore QoS and retain
   AT+MQTTPUB=1,1,,,topic_test,{head\,{body}\,{tail}}
   +MQTTPUB:OK
   +MQTTRECV:1,1,topic_test,{head,{body},{tail}},20,2,0,0
   ACK

.. _mqtt_at_mqttcfg:

AT+MQTTCFG
--------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Configure the parameters of MQTT entity.

Command
~~~~~~~~~~~~~~
.. code::

   AT+MQTTCFG=<con_id>,?
   AT+MQTTCFG=<con_id>,version,<version>
   AT+MQTTCFG=<con_id>,keepalive,<keepalive>
   AT+MQTTCFG=<con_id>,session,<session>
   AT+MQTTCFG=<con_id>,timeout,<timeout>
   AT+MQTTCFG=<con_id>,will,0
   AT+MQTTCFG=<con_id>,will,1,<qos>,<retain>,<topic>,<message>
   AT+MQTTCFG=<con_id>,ssl,<ssl>

Response
~~~~~~~~~~~~~~~~
.. code::

   // If execute sub-command "?"
   +MQTTCFG:MQTTVersion <version>
   +MQTTCFG:keepAliveInterval <timeout>
   +MQTTCFG:cleansession <session>
   +MQTTCFG:command_timeout_ms <timeout> (ms)
   +MQTTCFG:willFlag <will>
   +MQTTCFG:useSsl <ssl>
   // Then OK
   +MQTTCFG:OK

Or

.. code::

   +MQTTCFG:ERROR:<error_no>

Parameter
~~~~~~~~~~~~~~~~~~
<con_id>: The connect entity id.

   - [0,3]

? / version / keepalive / session / timeout / will / ssl: Sub-commands.

   - "?": Get the current parameters of <con_id> entity.

   - "version": Followed by <version>.

   - "session": Followed by <session>.

   - "timeout": Followed by <timeout>.

   - "will": Followed by <will> and its sub parameters.

   - "ssl": Followed by <ssl>.

<version>: MQTT version.

   - [3,4]

<keepalive>: Keepalive value.

   - [1,3600]

<session>: Session value.

   - [0,1]

<timeout>: The timeout value in millisecond.

   - [10000,60000]

<will>: The will value.

   - 0 or 1.

   - When it is 1, it is followed by <qos>, <retain>, <topic> and <message>.

<qos>: QoS value for LWT message.

   - [0,2]

<retain>: Retain value for LWT message.

   - [0,1]

<topic>: The LWT topic.

   - A string.

<message>: The LWT message.

   - A string.

<ssl>: Whether support SSL.

   - 0: Not support SSL.

   - 1: Support SSL.

Error Number
~~~~~~~~~~~~~~~~~~~~~~~~
- 1: Common error in software.

- 2: Error parameters.

Example
~~~~~~~~~~~~~~
.. code::

   // Create an MQTT entity with <con_id> = 1 at first.
   // Inquiry the current parameter.
   AT+MQTTCFG=1,?
   +MQTTCFG:MQTTVersion 4
   +MQTTCFG:keepAliveInterval 60
   +MQTTCFG:cleansession 1
   +MQTTCFG:command_timeout_ms 60000 (ms)
   +MQTTCFG:willFlag 0
   +MQTTCFG:useSsl 0
   +MQTTCFG:OK
   // Then modify the timeout to 50000
   AT+MQTTCFG=1,timeout,50000
   +MQTTCFG:OK
   // Inquiry new parameters.
   AT+MQTTCFG=1,?
   +MQTTCFG:MQTTVersion 4
   +MQTTCFG:keepAliveInterval 60
   +MQTTCFG:cleansession 1
   +MQTTCFG:command_timeout_ms 50000 (ms)
   +MQTTCFG:willFlag 0
   +MQTTCFG:useSsl 0
   +MQTTCFG:OK

.. _mqtt_at_mqttreset:

AT+MQTTRESET
------------------------
Description
~~~~~~~~~~~~~~~~~~~~~~
Reset all MQTT entities.

Command
~~~~~~~~~~~~~~
.. code::

   AT+MQTTRESET

Response
~~~~~~~~~~~~~~~~
.. code::

   +MQTTRESET:OK

Note
~~~~~~~~
.. note::
   If there are any running MQTT entities, there will be all disconnected and deleted right now.
