.. _cap_test_tool:

Introduction
------------------------
Cap Test Tool is the official Cap-Touch calibration tool developed by Realtek for Ameba series SoC. By communication with corresponding Cap-Touch test daemon on device via UART port, Cap Test Tool can calibrate the general and channel-specific Cap-Touch configurations.


The UI of Cap Test Tool is shown below.

.. figure:: ../figures/cap_test_tool_ui.png
   :scale: 25%
   :align: center
   :name: cap_test_tool_ui

   Cap Test Tool UI

Environment Setup
----------------------------------
Hardware Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The hardware setup is shown below.

.. figure:: ../figures/hardware_setup.svg
   :scale: 130%
   :align: center

   Hardware setup

The default UART pins of different ICs for Cap-Touch are listed below:

.. table:: Default UART pins of different ICs
   :width: 100%
   :widths: auto

   +----------------------+------------------------------------------------------------------------+
   | IC                   | Default UART pins                                                      |
   +======================+========================================================================+
   | AmebaSmart           | - CAP_UART_RX = PB10                                                   |
   |                      |                                                                        |
   |                      | - CAP_UART_TX = PB11                                                   |
   +----------------------+------------------------------------------------------------------------+
   | AmebaLite            | - CAP_UART_RX = PA0                                                    |
   |                      |                                                                        |
   |                      | - CAP_UART_TX = PA1                                                    |
   +----------------------+------------------------------------------------------------------------+
   | AmebaDPlus           | - CAP_UART_RX = PB30                                                   |
   |                      |                                                                        |
   |                      | - CAP_UART_TX = PB31                                                   |
   +----------------------+------------------------------------------------------------------------+


Software Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Host:

   - Environment requirements: EX. WinXP, Win 7 or later, Microsoft .NET Framework 4.0.

   - Software location: ``{SDK}/tools/ameba/CapTestTool/CapTestTool.exe``

- Device:

   - Build images with cap_test_daemon example, refer to ``{SDK}/component/example/cap_test_daemon/readme.txt`` for details.

Principle
------------------
The capacitance capture circuit adopts constant current source charging and ADC sampling voltage, the simple diagram is shown below.

- The constant current source I_mbias can be configured to charge the Vt net periodically, and there are parasitic capacitance Cp and touch capacitance Ctouch on the Vt net.
- Usually for a well-designed PCB, the ratio of Ctouch to Cp is about 1:10 to 1:20, so in fact, the proportion of useful signals is very small.

- The ADC synchronized with the charge and discharge controller samples the voltage of the Vt net and collects the maximum voltage at the end of the charge.

- ADC converts analog voltage into digital code identified by MCU for subsequent processing.

.. figure:: ../figures/simple_diagram.svg
   :scale: 120%
   :align: center

   Simple diagram

.. figure:: ../figures/waveform_of_vt.svg
   :scale: 120%
   :align: center

   Waveform of `Vt`

As shown below, the Cap-Touch Controller (CTC) scan period consists of active time and sleep time, which can be configured individually for different applications.

.. figure:: ../figures/scan_period_diagram.svg
   :scale: 120%
   :align: center

   Scan period diagram

With the disturbance of the surrounding environment, such as temperature, moisture, overlay, or other slight environmental noise, sensor capacitance change is caused.
ETC module is designed to track environmental changes and make calibrations.


ETC system tracks the capacitance change and updates the baseline and touch-threshold parameters based on the ETC algorithm periodically.
ETC scan interval can be configured by ETC Interval parameter. Users can decide how many intervals of scan periods they need to update the baseline in order to save power consumption.

Manual tuning of ETC parameters is also supported to meet different environments or special applications.
Increasing the baseline update step can accelerate the speed of baseline updating. Weighting factor is used as the baseline update principle in the judgment logic module.
For each ETC scan period, if the noise difference (`baseline` - `signal`) is larger than the factor, the baseline will increase.
If the noise difference (`baseline` ─ `signal`) is smaller than the factor, the baseline will decrease.

Configuration
--------------------------
Parameters
~~~~~~~~~~~~~~~~~~~~
  
.. table:: General configuration
   :width: 100%
   :widths: auto
   :class: longtable
   :name: cap_test_tool_general_configuration

   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Parameter            | Value                        | Comment                                                                                                   |
   +======================+==============================+===========================================================================================================+
   | Scan Interval        | 0~4095ms                     | The sleep time of channel after the sensor scanning and data processing. Recommended sleep time is        |
   |                      |                              |                                                                                                           |
   |                      |                              | 20~500ms for better response time.                                                                        |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Average Samples      | 4/8/16/32/64/128/256/512     | The sample number of raw data which is used to capture ADC for best accuracy and noise immunity.          |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Debounce Enable      | 0/1                          | The debounce feature avoids false triggering of sensors caused by noise spikes or system glitches.        |
   |                      |                              |                                                                                                           |
   |                      |                              | - 0: Disabled                                                                                             |
   |                      |                              |                                                                                                           |
   |                      |                              | - 1: Enabled                                                                                              |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Debounce Count       | 2/3/4/5                      | The shorter debounce times, the faster device responds to a sensor touch events.                          |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | ETC Enable           | 0/1                          | Environment tracking and calibration.                                                                     |
   |                      |                              |                                                                                                           |
   |                      |                              | - 0: Disabled                                                                                             |
   |                      |                              |                                                                                                           |
   |                      |                              | - 1: Enabled                                                                                              |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | ETC Interval         | 0~127                        | The count of scan intervals to do ETC update.                                                             |
   |                      |                              |                                                                                                           |
   |                      |                              | Scan period contains active time and scan interval.                                                       |
   |                      |                              |                                                                                                           |
   |                      |                              | ETC_update_interval=(scan_inteval+1)*scan_period                                                          |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Baseline Update Step | 0~15                         | Baseline update step (2^n) in ETC update principle. Use this parameter to configure baseline update step. |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | ETC Factor           | 0~15                         | Factor weight (2^n) for baseline update principle.                                                        |
   |                      |                              |                                                                                                           |
   |                      |                              | For each ETC scan period, if the noise difference (baseline-signal) is larger than Factor, the baseline   |
   |                      |                              |                                                                                                           |
   |                      |                              | increases. If the noise difference (baseline-signal) is less than Factor, the baseline decreases.         |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Clock Source         | - AmebaSmart/AmebaLite: OSC  | Sample clock:                                                                                             |
   |                      |                              |                                                                                                           |
   |                      | - AmebaDPlus:                | - AmebaSmart/AmebaLite: OSC 131kHz                                                                        |
   |                      |                              |                                                                                                           |
   |                      |   - OSC                      | - AmebaDPlus:                                                                                             |
   |                      |                              |                                                                                                           |
   |                      |   - XTAL                     |   - OSC 131kHz                                                                                            |
   |                      |                              |                                                                                                           |
   |                      |                              |   - XTAL 2MHz Divider                                                                                     |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Divider              | 1MHz/500KHz/250KHz/167KHz/   | Sample clock for XTAL 2MHz Divider:                                                                       |
   |                      |                              |                                                                                                           |
   |                      | 125KHz/62.5KHz/31.25KHz      | Max sample clock is 1MHz, charge time t = 0.5us.                                                          |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Proofing Enable      | Disabled                     | - AmebaSmart/AmebaLite: Not supported                                                                     |
   |                      |                              |                                                                                                           |
   |                      |                              | - AmebaDPlus: Enabled not supported now                                                                   |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Filter Enable        | - AmebaSmart/AmebaLite: 0    | - AmebaSmart/AmebaLite: Not supported                                                                     |
   |                      |                              |                                                                                                           |
   |                      | - AmebaDPlus:                | - AmebaDPlus:                                                                                             |
   |                      |                              |                                                                                                           |
   |                      |   - 0                        |   - 0: Filter disabled                                                                                    |
   |                      |                              |                                                                                                           |   
   |                      |   - 1                        |   - 1: Filter enabled                                                                                     |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Average Enable       | - AmebaDPlus:                | - AmebaSmart/AmebaLite: Not supported                                                                     |
   |                      |                              |                                                                                                           |
   |                      |   - 0                        | - AmebaDPlus: Average filter for periodic noise (50Hz or 60Hz), active when filter enabled                |
   |                      |                              |                                                                                                           |
   |                      |   - 1                        |   - 0: Disabled                                                                                           |
   |                      |                              |                                                                                                           |
   |                      |                              |   - 1: Enabled                                                                                            |   
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Average MDEC         | AmebaDPlus: 0~32767          | - AmebaSmart/AmebaLite: Not supported                                                                     |
   |                      |                              |                                                                                                           |
   |                      |                              | - AmebaDPlus: Active when average filter enabled                                                          |
   |                      |                              |                                                                                                           |
   |                      |                              |   - 0: Disable average filter                                                                             |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | Median Filter        | - AmebaDPlus:                | - AmebaSmart/AmebaLite: Not supported                                                                     |
   |                      |                              |                                                                                                           |
   |                      |   - 0                        | - AmebaDPlus: active when filter enabled                                                                  |
   |                      |                              |                                                                                                           |
   |                      |   - 1                        |   - 0: Median filter disabled                                                                             |
   |                      |                              |                                                                                                           |
   |                      |                              |   - 1: Median filter enabled                                                                              |   
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | IIR Enable           | - AmebaDPlus:                | - AmebaSmart/AmebaLite: Not supported                                                                     |
   |                      |                              |                                                                                                           |
   |                      |   - 0                        | - AmebaDPlus: IIR filter for high frequency white noise, active when filter enabled                       |
   |                      |                              |                                                                                                           |
   |                      |   - 1                        |   - 0: IIR filter disabled                                                                                |
   |                      |                              |                                                                                                           |
   |                      |                              |   - 1: IIR filter enabled                                                                                 |   
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | IIR A1               | AmebaDPlus: 0~65535          | - AmebaSmart/AmebaLite: Not supported                                                                     |
   |                      |                              |                                                                                                           |
   |                      |                              | - AmebaDPlus: active when IIR filter enabled                                                              |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+
   | IIR Gain             | AmebaDPlus: 0~65535          | - AmebaSmart/AmebaLite: Not supported                                                                     |
   |                      |                              |                                                                                                           |
   |                      |                              | - AmebaDPlus: active when IIR filter enabled                                                              |
   +----------------------+------------------------------+-----------------------------------------------------------------------------------------------------------+

.. table:: Channel configuration
   :width: 100%
   :widths: auto
   :class: longtable
   :name: cap_test_tool_channel_configuration

   +-------------------+--------------------------------+--------------------------------------------------------------------------------------------+
   | Parameter         | Value                          | Description                                                                                |
   +===================+================================+============================================================================================+
   | Mbias             | - AmebaSmart/AmebaLite: 1~63   | Sensitivity setting for each channel.                                                      |
   |                   |                                |                                                                                            |
   |                   | - AmebaDPlus: 1~255            | 1 LSB = 0.25uA.                                                                            |
   |                   |                                |                                                                                            |
   |                   |                                | Different register bit map:                                                                |
   |                   |                                |                                                                                            |
   |                   |                                | - AmebaSmart/AmebaLite: 0.25uA/0.5uA/1uA/2uA/4uA/8uA                                       |
   |                   |                                |                                                                                            |
   |                   |                                | - AmebaDPlus: 0.25uA/0.5uA/1uA/2uA/4uA/8uA/16uA/32uA                                       |
   +-------------------+--------------------------------+--------------------------------------------------------------------------------------------+
   | Diff Threshold    | 0~4095                         | Difference threshold judgement mode operates when ETC function is enabled.                 |
   |                   |                                |                                                                                            |
   |                   |                                | Compare the average sample data with the difference threshold to judge touch or proximity. |
   +-------------------+--------------------------------+--------------------------------------------------------------------------------------------+
   | Abs Threshold     | 0~4095                         | Absolute threshold judgement mode operates when ETC function is disabled.                  |
   |                   |                                |                                                                                            |
   |                   |                                | Compare the average sample data with the absolute threshold to judge touch or proximity.   |
   +-------------------+--------------------------------+--------------------------------------------------------------------------------------------+
   | N Noise Threshold | 0~4095                         | Raw data of the maximum capacitance change caused by the environmental change.             |
   +-------------------+--------------------------------+--------------------------------------------------------------------------------------------+
   | P Noise Threshold | 0~4095                         | Raw data of the maximum capacitance change caused by the environmental change.             |
   +-------------------+--------------------------------+--------------------------------------------------------------------------------------------+
   | Sample Data       | 0~4095                         | Real finger touch voltage.                                                                 |
   |                   |                                |                                                                                            |
   |                   |                                | Also named average data.                                                                   |
   +-------------------+--------------------------------+--------------------------------------------------------------------------------------------+
   | Baseline Data     | 0~4095                         | The reference voltage.                                                                     |
   |                   |                                |                                                                                            |
   |                   |                                | Active when ETC enabled.                                                                   |
   +-------------------+--------------------------------+--------------------------------------------------------------------------------------------+
   | Diff Data         | -4095~4095                     | Difference data between average data (sample data) and baseline data.                      |
   |                   |                                |                                                                                            |
   |                   |                                | Active when ETC enabled.                                                                   |
   |                   |                                |                                                                                            |
   |                   |                                | Diff Data = Baseline Data - Average Data                                                   |
   +-------------------+--------------------------------+--------------------------------------------------------------------------------------------+
   | SNR               | -                              | SNR monitor operates effectively during project development or MP.                         |
   |                   |                                |                                                                                            |
   |                   |                                | :math:`SNR= |Diff Data (touch signal)|/|Noise (peak-to-peak)|`                             |
   +-------------------+--------------------------------+--------------------------------------------------------------------------------------------+

Reload Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Make sure the device is connected.

2. Go to the :guilabel:`Configuration` tab.

3. Click the :guilabel:`Reload` button.

   .. note::
         - The configuration will be auto-reloaded when :guilabel:`Open` button is clicked.

         - When you click :guilabel:`Apply` or :guilabel:`Reload` button, both general configurations and channel configurations will take effect simultaneously.


Apply Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Make sure device is connected.

2. Go to the ``Configuration`` tab.

3. Change the value of parameters listed in Table :ref:`cap_test_tool_general_configuration` and :ref:`cap_test_tool_channel_configuration`.

4. Click the :guilabel:`Apply` button.


Calibration
----------------------
Using tool to adjust Iref and threshold, it is more convenient to adjust the parameters that meet the performance requirements.

.. note::
   The same set of hardware circuit corresponds to the same set of parameter values. After the hardware circuit is replaced, the calibration parameter values need to be reset.

Cap Test Tool is used as a tool to improve the debugging speed in the development stage, after the parameter calibration of
a model product, users need to fill in the suggested parameters given by tool in the SDK code, so as to solidify a set of parameters in FLASH to realize batch operation.

Operational details of the SDK can be provided in the application note.

Iref Calibration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Iref determines the sensitivity.

Theoretically, the larger `Iref` is, the higher the sensitivity will be. But too high `Iref` will cause the charging voltage
to exceed the measurement range of ADC, so a reasonable `Iref` should meet the following principles:

- The sampling value of the untouched state accounts for about 80% of the ADC maximum range. Because the ADC resolution is 12 bits, and the maximum range number code is 4095, it is safer that the sampling value of the untouched state is set at about 3300.

.. note::
   The value filled in the register is only used for tool. When the IC is powered off, the register will be cleared. Therefore, if you want to save the calibration result value, you need to fill the result parameters (`Mbias`) into the SDK.

The calibration process of Iref is integrated in the tool, and the user is only required to complete the following calibration process:

1. Make sure device is connected.

2. Go to the ``Configuration`` tab.

3. Select the checkbox of channels which need to be enabled.

4. Click the ``Iref Calibration`` button.


   .. caution::
      Don’t touch Cap-Touch pins during Iref calibration process.


5. Observe the logs and wait the process to complete.

6. Both mbias and baseline will be calibrated in device, and mbias will be updated in Cap Test Tool.

   .. figure:: ../figures/iref_calibration_operation.png
      :scale: 25%
      :align: center
      :name: iref_calibration_operation

      Iref calibration operation

Threshold Calibration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The threshold (Diff threshold) determines the reliability and flexibility of the touch operation. Too high threshold may cause the touch to be accurately identified, and too low threshold may cause false trigger operation.
Therefore, a reasonable threshold should be personalized according to the test results of the actual circuit. Generally, it is recommended to set the threshold at 80% of the touch value.

Calibration program adopts the way of touch with manual operation, because the tool does not know the size of the touch signal in advance, the user needs to make 2 or 5 standard touches operation
after clicking the button to start the task of calibrating the threshold. The task will record the average touch, and after the user clicks the button again to end the task,
a reasonable threshold will be automatically filled in the register.

The threshold also includes the noise threshold, which is used to limit the noise range and realize the noise tracking and filtering of the algorithm,
usually without too much attention from the user. The user only needs to divide the calibrated `Diff threshold` by 2 and fill in the SDK as `N Noise threshold` and `P Noise threshold` respectively.

The absolute value threshold is the debugging function, which the user does not need to pay attention to, and this parameter limits the touch behavior when the ETC function is disabled.

.. note::

   The value filled in the register is only used for tool.
   When the IC is powered off, the register will be cleared.
   Therefore, if you want to save the calibration result value, you need to fill the result parameters (`Diff threshold`, `N Noise threshold` and `P Noise threshold`) into the SDK.

1. Make sure the device is connected.

2. Go to the ``Configuration`` tab.

3. Select the checkbox of channels which need to be enabled.

4. Click the ``Start Threshold Calibration`` button.

   The tool starts to print logs.

5. Touch channels.

   If you want to observe the signals, continue :ref:`Step 6 <cap_test_tool_step_6>`; otherwise, jump to :ref:`Step 8 <cap_test_tool_step_8>`.

   .. figure:: ../figures/threshold_calibration_operation_before_calibration.png
      :scale: 30%
      :align: center
      :name: threshold_calibration_operation_before_calibration

      Threshold calibration operation (before calibration)

.. _cap_test_tool_step_6:

6. Switch to the ``Monitor`` tab.

   It only shows ``Diff Data vs Diff Threshold`` view. Change the ``Select Channel(s)`` box to switch channels.

   .. note::
         - Diff threshold will be set to the value of 80% of max. diff data.

         - Noise threshold will be set to the value of 40% of max. diff data.

   .. figure:: ../figures/threshold_calibration_operation_in_calibration.png
      :scale: 30%
      :align: center

      Threshold calibration operation (in calibration)

7. Switch to the ``Configuration`` tab.

.. _cap_test_tool_step_8:

8. Click the ``Stop Threshold Calibration`` button.

9. Cap Test Tool calculates diff threshold and noise threshold, prints log and updates values in cells.

   .. figure:: ../figures/threshold_calibration_operation_after_calibration.png
      :scale: 30%
      :align: center

      Threshold calibration operation (after calibration)

   .. note::

         - Threshold calibration only works in ETC-enabled mode.

         - Diff threshold, N Noise threshold and P Noise threshold will be calculated and set to device based on the note in :ref:`Step 6 <cap_test_tool_step_6>`.

         - Abs Threshold is auto-set in device and won't be updated after threshold calibration. Please click the ``Reload`` button if you want to load Abs Threshold value.

   .. caution::

      Remember to click the ``Stop Threshold Calibration`` button when completes, otherwise the threshold value won't be calculated.


Monitor
--------------
Parameters
~~~~~~~~~~~~~~~~~~~~

.. table:: Monitor parameters
   :width: 100%
   :widths: auto

   +-------------------+-------------------------------+-----------------------------------------------------------------+
   | Parameter         | Value                         | Comment                                                         |
   +===================+===============================+=================================================================+
   | Debug Enable      | 0/1                           | Disabled now.                                                   |
   |                   |                               |                                                                 |
   |                   |                               | - 0: Debug mode disabled/normal mode enabled                    |
   |                   |                               |                                                                 |
   |                   |                               | - 1: Debug mode enabled/normal mode disabled                    |
   +-------------------+-------------------------------+-----------------------------------------------------------------+
   | Debug Mode        | Manual/Auto                   | Active when debug enabled.                                      |
   |                   |                               |                                                                 |
   |                   |                               | Debug mode usually works during debug/development process.      |
   +-------------------+-------------------------------+-----------------------------------------------------------------+
   | Select View       | - Sample Data                 | Different views of signals.                                     |
   |                   |                               |                                                                 |
   |                   | - Average Data vs Baseline    |                                                                 |
   |                   |                               |                                                                 |
   |                   | - Diff Data vs Diff Threshold |                                                                 |
   |                   |                               |                                                                 |
   |                   | - SNR                         |                                                                 |
   +-------------------+-------------------------------+-----------------------------------------------------------------+
   | Displayed Samples | 0~400                         | The sample number of raw data which is captured in active time. |
   +-------------------+-------------------------------+-----------------------------------------------------------------+
   | Sample Interval   | 10~10000ms                    | Sample interval in active time.                                 |
   +-------------------+-------------------------------+-----------------------------------------------------------------+

Reset Baseline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Make sure the device is connected.

2. Go to the ``Monitor`` tab.

3. Click the :menuselection:`Reset Baseline` button.

   .. note::

         - It will reset the baseline of all channels.

         - It has no association with the current monitor view.


   .. figure:: ../figures/reset_baseline_operation.png
      :scale: 35%
      :align: center

      Reset baseline operation

Observe Signals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Make sure the device is connected.

2. Go to the :menuselection:`Configuration`:menuselection:` tab, and select the checkbox of channels which need to be enabled.

3. Go to the :menuselection:`Monitor` tab.

4. Change the ``select View`` box, and set the values of ``Displayed Samples`` and ``Sample Interval``.

5. Click the :menuselection:`Start` button and touch channels.

6. Click the :menuselection:`Stop` button when completes.


Monitor boards of different views are shown in the following figures.

.. figure:: ../figures/monitor_board_sample_data_view.png
   :scale: 30%
   :align: center

   Monitor board (``Sample Data`` View)

.. figure:: ../figures/monitor_board_data_baseline_view.png
   :scale: 30%
   :align: center

   Monitor board (``Average Data vs Baseline`` View)

.. figure:: ../figures/monitor_board_diff_threshold_view.png
   :scale: 30%
   :align: center

   Monitor board (``Diff Data vs Diff Threshold`` View)

.. figure:: ../figures/monitor_board_snr_view.png
   :scale: 30%
   :align: center

   Monitor board (``SNR`` View)

.. note::

      - In ``Sample Data`` and ``Average Data vs Baseline`` view, ``Select Channel(s)`` could be chosen before/in monitoring status.

      - In ``Diff Data vs Diff Threshold`` view, the specific channel configuration could be customized by user before monitor starts.

      - In ``SNR`` view, ``Select Channel(s)`` is disabled since the signal-to-noise ratio is global data.
