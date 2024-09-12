.. _chip_enable:

Introduction
------------------------
The CHIP_EN (chip enable) is an external pin that can be used to control the reset status of the whole SoC. This pin can work in level reset mode, interrupt reset mode or pulse reset mode. By default, it works in level reset mode. This pin always has the function of resetting system no matter in which mode.


In |CHIP_NAME|, the button with ``CHIP_EN`` is connected to the ``CHIP_EN`` pin, as :ref:`clip_en_on_board` shows.

.. figure:: ../figures/clip_en_on_board.png
   :scale: 50%
   :align: center
   :name: clip_en_on_board

   CHIP_EN on board

Three Working Modes
--------------------------------------
There are three working modes of CHIP_EN for different usages.

Level Reset Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Level reset mode is the default mode of CHIP_EN. In this mode, a low level on this pin longer than debounce time will trigger RESET directly and the SoC will reboot when this pin goes from low to high.


User can reset the whole chip by simply pressing down and releasing the CHIP_EN button. When low level is detected longer than debounce time, the chip will be reset after the CHIP_EN button is released. So user can adjust the sensitivity of CHIP_EN by setting different debounce time from 100us to 16ms.

Interrupt Reset Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In interrupt reset mode, a low level on this pin longer than the sum of debounce and short press time can trigger an interrupt instead of resetting the system directly. Thus, software can handle the interrupt and choose whether to reset the system.


The interrupt reset mode is mainly designed for the power save scenario. The CHIP_EN button just likes the power button of the smartphone: a short press will trigger the system to enter low power mode or wake up the system; a long press will trigger an interrupt to remind the user whether to reset the system. The reboot will happen if user chooses reboot or the system crashed.

Pulse Reset Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In pulse reset mode, a low level on this pin longer than debounce time will trigger RESET directly and the SoC will reboot immediately. User can read the status of the CHIPEN pin in boot code to distinguish short/long press. This mode usually can be found in router. Short press will cause the system cold boot; long press will cause the system code boot and restore factory settings.


Once the chip is configured working in Pulse Reset Mode, software cannot change the mode anymore. Only power off will take the chip to Level Reset Mode.

How to Choose Work Mode
----------------------------------------------
- For device does not need any control on this pin, tie this pin to ``high``.

- For simply reset requirement, use the ``default level reset mode``.

- If both reset and re-storage of factory settings are needed, use the ``pulse reset mode``.

- For low power scenario, power control and reset are needed on a single pin, use the ``interrupt reset mode``.

CHIP_EN Driver APIs
--------------------------------------
CHIPEN_WorkMode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table::
   :width: 100%
   :widths: auto

   +--------------+---------------------------------------------+
   | Items        | Description                                 |
   +==============+=============================================+
   | Introduction | Configure CHIP_EN work mode                 |
   |              |                                             |
   |              | CHIP_EN works in HW reset mode by default.  |
   +--------------+---------------------------------------------+
   | Parameters   | mode: new work mode of CHIPEN, which can be |
   |              |                                             |
   |              | - CHIPEN_HW_RESET_MODE                      |
   |              |                                             |
   |              | - CHIPEN_INT_RESET_MODE                     |
   |              |                                             |
   |              | - CHIPEN_PULSE_RESET_MODE                   |
   +--------------+---------------------------------------------+
   | Return       | None                                        |
   +--------------+---------------------------------------------+

CHIPEN_DebounceSet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table::
   :width: 100%
   :widths: auto

   +--------------+-------------------------------------------------------------+
   | Items        | Description                                                 |
   +==============+=============================================================+
   | Introduction | Set the CHIP_EN debounce Time, which works in all work mode |
   +--------------+-------------------------------------------------------------+
   | Parameters   | debounce: new debounce counter, which can be                |
   |              |                                                             |
   |              | - CHIPEN_DBC_0US                                            |
   |              |                                                             |
   |              | - CHIPEN_DBC_100US                                          |
   |              |                                                             |
   |              | - CHIPEN_DBC_500US                                          |
   |              |                                                             |
   |              | - CHIPEN_DBC_1MS                                            |
   |              |                                                             |
   |              | - CHIPEN_DBC_2MS                                            |
   |              |                                                             |
   |              | - CHIPEN_DBC_4MS                                            |
   |              |                                                             |
   |              | - CHIPEN_DBC_8MS                                            |
   |              |                                                             |
   |              | - CHIPEN_DBC_16MS                                           |
   +--------------+-------------------------------------------------------------+
   | Return       | None                                                        |
   +--------------+-------------------------------------------------------------+

CHIPEN_ThresHoldSet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table::
   :width: 100%
   :widths: auto
   :class: longtable

   +--------------+------------------------------------------------------------------------------------+
   | Items        | Description                                                                        |
   +==============+====================================================================================+
   | Introduction | Set long press and short press threshold, which only works in interrupt reset mode |
   +--------------+------------------------------------------------------------------------------------+
   | Parameters   | - Thres_LP: long press threshold                                                   |
   |              |                                                                                    |
   |              |    - CHIPEN_LP_1S                                                                  |
   |              |                                                                                    |
   |              |    - CHIPEN_LP_1P5S                                                                |
   |              |                                                                                    |
   |              |    - CHIPEN_LP_2S                                                                  |
   |              |                                                                                    |
   |              |    - CHIPEN_LP_2P5S                                                                |
   |              |                                                                                    |
   |              |    - CHIPEN_LP_3S                                                                  |
   |              |                                                                                    |
   |              |    - CHIPEN_LP_3P5S                                                                |
   |              |                                                                                    |
   |              |    - CHIPEN_LP_4S                                                                  |
   |              |                                                                                    |
   |              |    - CHIPEN_LP_4P5S                                                                |
   |              |                                                                                    |
   |              | - Thres_SP: short press threshold                                                  |
   |              |                                                                                    |
   |              |    - CHIPEN_SP_50MS                                                                |
   |              |                                                                                    |
   |              |    - CHIPEN_SP_100MS                                                               |
   |              |                                                                                    |
   |              |    - CHIPEN_SP_150MS                                                               |
   |              |                                                                                    |
   |              |    - CHIPEN_SP_200MS                                                               |
   |              |                                                                                    |
   |              |    - CHIPEN_SP_250MS                                                               |
   |              |                                                                                    |
   |              |    - CHIPEN_SP_300MS                                                               |
   |              |                                                                                    |
   |              |    - CHIPEN_SP_350MS                                                               |
   +--------------+------------------------------------------------------------------------------------+
   | Return       | None                                                                               |
   +--------------+------------------------------------------------------------------------------------+

CHIPEN_AckTimeSet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table::
   :width: 100%
   :widths: auto

   +--------------+------------------------------------------------------------------------------+
   | Items        | Description                                                                  |
   +==============+==============================================================================+
   | Introduction | Set the ACK threshold for long press interrupt.                              |
   |              |                                                                              |
   |              | If long press interrupt can't be cleared within Tack, the system will reboot |
   +--------------+------------------------------------------------------------------------------+
   | Parameters   | Tack:                                                                        |
   |              |                                                                              |
   |              | - CHIPEN_ACK_50MS                                                            |
   |              |                                                                              |
   |              | - CHIPEN_ACK_100MS                                                           |
   |              |                                                                              |
   |              | - CHIPEN_ACK_200MS                                                           |
   |              |                                                                              |
   |              | - CHIPEN_ACK_400MS                                                           |
   +--------------+------------------------------------------------------------------------------+
   | Return       | None                                                                         |
   +--------------+------------------------------------------------------------------------------+

CHIPEN_ClearINT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table::
   :width: 100%
   :widths: auto

   +--------------+----------------------------------+
   | Items        | Description                      |
   +==============+==================================+
   | Introduction | Clear CHIP_EN interrupt status   |
   +--------------+----------------------------------+
   | Parameters   | INTrBit: interrupt to be cleared |
   +--------------+----------------------------------+
   | Return       | None                             |
   +--------------+----------------------------------+

CHIPEN_GetINT
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table::
   :width: 100%
   :widths: auto

   +--------------+------------------------------+
   | Items        | Description                  |
   +==============+==============================+
   | Introduction | Get CHIP_EN interrupt status |
   +--------------+------------------------------+
   | Parameters   | None                         |
   +--------------+------------------------------+
   | Return       | Interrupt status             |
   +--------------+------------------------------+

