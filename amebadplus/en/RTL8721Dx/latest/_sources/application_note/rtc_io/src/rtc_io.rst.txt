.. _rtc_io:

Introduction
------------------------
The RTC_IO module serves to store the RTC time and count the power-off time temporarily when the chip is in power off period.
After repower on, the stored time data and counter during power-off can be read back according to a certain procedure.


Through the read back time information, current time can be calculated and set to the RTC module.
Therefore, the timer starts to run as new time, which guarantees that the time information will not be affected by chip power down.

Usage
----------
There are two sceneries and respective operation flows when using the RTC_IO module, and this section introduces the detailed usage.


To keep RTC_IO powered on when the chip is powered off, it is supposed to perform the following connections via Dupont Lines:

- Connect the power supply pin of ``VDH_RTC`` to 3.3V power supply

- Connect the GND of the development board to the common ground of the 3.3V power supply


For the first time power on, follow these steps:

1. Write 6'd0 (Reset) to register ``rtc_io_test_din`` bit field, and shift into RTC_IO

   .. code-block:: c
   
      RTCIO_SetRValue(RTCIO_RECV_RVAL_RST);      

.. _rtc_io_first_time_power_on_step_2:

2. Perform 131K calibration, in order to acquire the calibration parameter which will be shifted into RTC_IO

   .. code-block:: c
   
      OSC131K_Calibration(30000);


3. Acquire the RVAL produced by Step :ref:`2 <rtc_io_first_time_power_on_step_2>` and shift into RTC_IO.

   .. code-block:: c
   
      RTCIO_SetRValue(RTCIO_RECV_RVAL_CAL);


4. Prepare time data that will be set to the device through the RTC module

   .. code-block:: c

      RTC_TimeTypeDef RTC_TimeStruct;
      RTC_TimeStructInit(&RTC_TimeStruct);
      RTC_TimeStruct.RTC_Year = 2024;
      RTC_TimeStruct.RTC_Hours = 10;
      RTC_TimeStruct.RTC_Minutes = 20;
      RTC_TimeStruct.RTC_Seconds = 30;

.. _rtc_io_first_time_power_on_step_5:

5. Initialize and enable RTC module

   .. code-block:: c

      RCC_PeriphClockCmd(APBPeriph_RTC, APBPeriph_RTC_CLOCK, ENABLE);
      RTC_StructInit(&RTC_InitStruct);
      RTC_Init(&RTC_InitStruct);
      RTC_SetTime(RTC_Format_BIN, &RTC_TimeStruct);

In case of the chip repower on, but RTC_IO domain keeps powering on during power off period, it is supposed to follow these steps:

1. Check the :func:`BOOT_Reason()` return value.

   Continue the next steps when return 0, otherwise do nothing.

2. Check the :func:`RTCIO_IsEnabled()` return value.

   Continue the next steps when return TRUE, otherwise perform the procedures as mentioned above for the first time power on.

3. Shift out the stored time data and counter during power off period

   .. code-block:: c

      RTCIO_TimeInfo RTCIO_TimeStruct;
      RTC_TimeTypeDef RTC_TimeStruct;
      if(BOOT_Reason() == 0)
      {
      if (RTCIO_IsEnabled() == TRUE)
      {
      /* shift out bkup data */
      RTCIO_GetTimeInfo(&RTCIO_TimeStruct);
      /* calculate new Time */
      app_calc_new_time(&RTCIO_TimeStruct, &RTC_TimeStruct);
      }
      }

4. Calculate new time through the struct ``RTCIO_TimeStruct``, and the result store into struct ``RTC_TimeStruct``. The later will be set to the device.

   The function :func:`app_calc_new_time()` is just an example. It should be achieved according to actual application.

5. Initialize and enable the RTC module again as the Step :ref:`5 <rtc_io_first_time_power_on_step_5>` in first time power on, and set the above calculated new time to device.

