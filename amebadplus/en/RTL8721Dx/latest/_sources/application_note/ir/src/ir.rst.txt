.. _ir:

Introduction
------------------------
The Infrared Radiation (IR) provides hardware modulation for Infrared Radiation sending and hardware auto capture for receiving.


This chapter introduces how to use IR.

IR Sending
--------------------
.. _ir_tx_polling_mode:

Tx Polling Mode
~~~~~~~~~~~~~~~~
To use IR sending function, the following steps are mandatory.

1. Configure the IR pin according to the pinmux table.

   For example, in order to use *PB4* as IR Tx pin, call the following function. It is the same for other IR pins.

   .. code-block:: c

      Pinmux_Config(_PB_4, PINMUX_FUNCTION_IR_TX);

.. _ir_sending_step_2:

2. Call :func:`IR_Cmd()` to disable IR.

.. _ir_sending_step_3:

3. Set parameters, and modify some parameters if needed.

   .. code-block:: c

      IR_StructInit(IR_InitTypeDef *IR_InitStruct);

4. Initialize the hardware using the parameters in :ref:`Step 3 <ir_sending_step_3>`.

   .. code-block:: c

      IR_Init(IR_InitTypeDef *IR_InitStruct);

.. _ir_sending_step_5:

5. Write Tx data to FIFO by using :func:`IR_SendBuf()` or :func:`IR_SendData()`.

.. _ir_sending_step_6:

6. Call :func:`cIR_Cmd()` to enable IR to start transmission.

7. Write more data to FIFO if needed.


.. note::
      - In :ref:`Step 2 <ir_sending_step_2>` to :ref:`Step 6 <ir_sending_step_6>`, It is suggested that disabling IR at first, and then enabling IR after writing data to FIFO.

      - In :ref:`Step 5 <ir_sending_step_5>`, pay attention to convert the data into the appropriate format that Tx FIFO register can recognize before writing data to FIFO.


Special Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~
Tx FIFO Offset Issue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to judge whether Tx data in FIFO has been sent completely or not, you’d better check Tx FIFO empty flag rather than *TX_FIFO_OFFSET*.

Tx Last Packet Cannot Let FSM Enter Idle Issue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the last packet written to Tx FIFO cannot let Tx state machine enter idle, it is suggested write some data packets to Tx FIFO before enabling IR Tx.

Refer to :ref:`Step 2 <ir_sending_step_2>` ~ :ref:`Step 6 <ir_sending_step_6>` in Section :ref:`ir_tx_polling_mode`.

IR Receiving
------------------------
Rx Interrupt Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To use IR receiving function, the following steps are mandatory.

1. Configure the IR pin according to the pinmux table.

   For example, in order to use *PB5* as IR Rx pin, call the following function. It is the same for other IR pins.

   .. code-block:: c

      Pinmux_Config(_PB_5, PINMUX_FUNCTION_IR_RX);

.. _ir_receiving_step_2:

2. Set parameters, such as sampling frequency, Rx FIFO threshold level, Rx counter threshold type, Rx counter threshold level, and Rx trigger mode if needed.

   .. code-block:: c

      IR_StructInit(IR_InitTypeDef *IR_InitStruct);

3. Initialize the hardware using the parameters in :ref:`Step 2 <ir_receiving_step_2>`.

   .. code-block:: c

      IR_Init(IR_InitTypeDef *IR_InitStruct);

4. Configure the interrupt if needed and register the interrupt callback function.

   .. code-block:: c

      IR_INTConfig(IR_DEV, IR_RX_INT_ALL_EN, ENABLE);
      InterruptRegister((IRQ_FUN) IR_irq_handler, IR_IRQ, (u32)NULL, 10);
      InterruptEn(IR_IRQ, 10);

5. Call :func:`IR_Cmd()` to enable IR.

6. Call :func:`IR_ClearRxFIFO()` to clear Rx FIFO.

.. _ir_receiving_step_7:

7. When Rx FIFO threshold interrupt triggers, read data from Rx FIFO with :func:`IR_ReceiveBuf()` and :func:`IR_ReceiveData()`, and make further processing in interrupt handle function.

.. note::
      - In :ref:`Step 7 <ir_receiving_step_7>`, to decode the receiving data correctly, you should understand the data format in Rx FIFO register.

      - Waveform inverse issue: in Rx ending, if the waveform is inverse, you should define *INVERSE_DATA* in :file:`Ir_nec_protocol.h` and set ``IR_InitStruct.IR_RxCntThrType = IR_RX_COUNT_HIGH_LEVEL``.


Rx Learning
~~~~~~~~~~~~~~~~~~~~~~
The process of Rx learning is similar to common Rx. The difference is that in interrupt handle function, Rx learning should store each pulse of the Rx waveform, while common Rx only needs to store the carrier or un-carrier duration.

.. figure:: ../figures/difference_of_waveform_between_rx_learning_and_common_rx.svg
   :scale: 130%
   :align: center

   Difference of waveform between Rx learning and common Rx



.. note::
      - It is advised that putting the interrupt handle function code in RAM, and close other peripheral interrupts to avoid the interfere.

      - If the carrier frequency of learning waveform is larger than 400kHz, the hardware may cannot respond to the interrupt in time, which will result in decoding carrier frequency failed.

