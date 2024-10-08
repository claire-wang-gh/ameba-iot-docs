.. _adc:


Introduction
------------------------
This chapter describes the usage of the 12-bit analog-to-digital converter (ADC) of |CHIP_NAME|.

The ADC of the |CHIP_NAME| is a successive-approximation register (SAR) ADC, which includes up to 7 external channels, 1 battery measurement channel and 1 internal channel. The ADC supports continuous sampling, software triggered sampling and timer triggered sampling. The result of ADC conversion is stored in the result register and can be read on demand.

The following table shows the description of channels.

.. table:: Description of channels
   :width: 100%
   :widths: auto

   +-------------------------+----------------+-----------+-------------------+
   | Channel                 | ADC channel ID | Pin name  | Input voltage (V) |
   +=========================+================+===========+===================+
   | External normal channel | CH0~CH6        | PB13~PB19 | 0~3.3             |
   +-------------------------+----------------+-----------+-------------------+
   | External BAT_MEAS       | CH7            | BAT_MEAS  | 0 ~ 5             |
   +-------------------------+----------------+-----------+-------------------+
   | Internal AVDD33         | CH9            | N/A       | 0~3.3             |
   +-------------------------+----------------+-----------+-------------------+

Usage
----------

To use ADC auto mode, the following steps are mandatory.

1. Enable clock and function of ADC module.

   .. code-block:: C

      RCC_PeriphClockCmd(APBPeriph_ADC, APBPeriph_ADC_CLOCK, ENABLE);

2. Configure the ADC pinmux according to the pinmux specification.

   For example, call the following functions to use ADC0.

   .. code-block:: C

      Pinmux_Config(_PB_19, PINMUX_FUNCTION_ADC)
      PAD_InputCtrl(_PB_19, DISABLE);
      PAD_PullCtrl(_PB_19, GPIO_PuPd_NOPULL);
      PAD_SleepPullCtrl(_PB_19, GPIO_PuPd_NOPULL);

3. Set the default parameters, and modify ADC mode. After that, channel list and other parameters can be modified in ``ADC_InitStruct`` if needed.

   .. code-block:: C

      ADC_StructInit(ADC_InitTypeDef *ADC_InitStruct);
      ADC_InitStruct->ADC_OpMode = ADC_AUTO_MODE;

4. Initialize ADC and then enable ADC.

   .. code-block:: C

      ADC_Init(ADC_InitTypeDef *ADC_InitStruct);
      ADC_Cmd(ENABLE);

5. Read ADC sample data. You can use polling mode or interrupt mode to acquire ADC sample data.

   - Polling mode:
   
      .. code-block:: C
   
         ADC_ReceiveBuf(u16 *pBuf, u32 len);
   
   - Interrupt mode:
   
      .. code-block:: C
   
         ADC_INTConfig(ADC_BIT_IT_FIFO_OVER_EN | ADC_BIT_IT_FIFO_FULL_EN, ENABLE);
         InterruptRegister((IRQ_FUN)ADCIrqRxHandler, ADC_IRQ, NULL, INT_PRI_MIDDLE);
         InterruptEn(ADC_IRQ, INT_PRI_MIDDLE);
         ADC_AutoCSwCmd(ENABLE);

