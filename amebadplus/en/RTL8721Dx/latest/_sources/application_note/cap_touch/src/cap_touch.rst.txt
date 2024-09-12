.. _cap_touch_controller:

Introduction
------------------------
The Cap-Touch Controller (CTC) provides 4 channels for capacitive sensing, which offers a wide range of capacitance detection. The sensitivity and threshold for each channel are configurable. For different applications and surroundings, you should tune parameters to achieve the best performance.


This chapter introduces how to use Cap-Touch.

Usage
----------
Cap Test Tool
~~~~~~~~~~~~~~~~~~~~~~~~~~
Cap Test Tool is the official Cap-Touch calibration tool developed by Realtek, which can calibrate the general and channel-specific Cap-Touch configurations.


We suggest doing CTC calibration by the Cap Test Tool directly and automatically. Refer to the application note of Cap Test Tool for more details about usage.


Of course, users can tune the configuration parameters manually to meet special requirements according to section :ref:`ctc_initialization` and :ref:`ctc_calibration`.

.. _ctc_initialization:

CTC Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The CTC initialization is implemented by the following steps:

.. _ctc_initialization_step_1:

1. Call ``CapTouch_StructInit()`` to initialize the configuration parameters of Cap-Touch, such as SampleCnt, ScanInterval, DiffThreshold, etc.

2. Set configuration parameters in the following table and update configuration parameters of Cap-Touch in step :ref:`1 <ctc_initialization_step_1>` with it, which include touch threshold, noise threshold, mbias current, and enable control for each channel. This method to tune parameters for each channel can be found in section :ref:`ctc_calibration`.

   .. code::

      const CapTouch_CHInitTypeDef ctc_ch_config[4] =
      {
      /*DiffThreshold, MbiasCurrent, ETCNNoiseThr, ETCPNoiseThr, CHEnable*/
      {80,      0x0C,      40,    40,    ENABLE}, /* Channel 0 */
      {80,      0x0C,      40,    40,    DISABLE}, /* Channel 1 */
      {80,      0x0C,      40,    40,    DISABLE}, /* Channel 2 */
      {80,      0x0C,      40,    40,    DISABLE}, /* Channel 3 */
      };


   .. note::

      The configuration parameters can be acquired in Cap Test Tool.

3. Call ``CapTouch_Init()`` to configure the Cap-Touch.

4. Enable Cap-Touch by ``CapTouch_Cmd()`` and enable the interrupt by ``CapTouch_INTConfig()``.

After all this, the Cap-Touch will start to work.

.. _ctc_calibration:

CTC Calibration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To achieve the best performance (sensitivity, reliability or response time), users need to tune touch threshold, noise threshold and mbias current during development.


Mbias current needs to be considered during development, because different circuits (such as PCB layout) have different parasitic capacitance and sensitivity. When the circuit design is confirmed, the user can use Realtek cap test tool to initialize the Mbias. The calibration principle is to adjust Mbias so that the signal value of baseline is about 3300~3600 without touch.


The recommended difference threshold is 80% of the difference threshold (baseline − touch signal), and 30%~40% for noise threshold. Users can increase or decrease the threshold value to meet the SNR requirement (SNR>5).



.. note::
      - For operation instructions, please refer to Captesttool_manual.

      - Too large mbias will cause the charging voltage to exceed the full range, which may cause damage to the circuit.

      - When using Cap-Touch, to prevent leakage, the Cap-Touch pin should be configured as shutdown or configured as no-pull, at the same time input and output of the pad should be disabled.


CTC Wakeup
~~~~~~~~~~~~~~~~~~~~
When using CTC as a wakeup source, configure the CTC and system as follows:

1. Initialize CTC and enable its interrupt according to :ref:`ctc_initialization`.

2. Set the related wakeup source (``WAKE_SRC_CTOUCH``) in ``sleep_wevent_config[]`` to ``WAKEUP_KM4`` or ``WAKEUP_KM0`` (based on which CPU you want to wake). The interrupt should be registered on the same CPU selected by ``sleep_wevent_config[]``.

3. Switch CTC clock source to CTC IP clock before system enters sleep mode by ``RCC_PeriphClockSource_CTC()``.

4. Enter sleep mode by releasing the wakelock in KM4 (PMU_OS needs to be released since it is acquired by default when boot).

5. Clear the CTC interrupt when wakeup and switching CTC clock source to LBUS clock by ``RCC_PeriphClockSource_CTC()``.

