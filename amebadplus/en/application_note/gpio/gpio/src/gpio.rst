.. _gpio:

Output
------------
To do GPIO output test, the following steps are mandatory.

1. Select GPIO pin, and set GPIO mode to output.

   .. code:: c

      GPIO_InitStruct.GPIO_Pin = GPIO_Pin;
      GPIO_InitStruct.GPIO_Mode = GPIO_Mode_OUT;

2. Initialize hardware using the parameters in step 1.

   .. code:: c

      GPIO_Init(GPIO_InitTypeDef *GPIO_InitStruct);

3. Write a logic value to a specified output port pin.

   .. code:: c

      GPIO_WriteBit(u32 GPIO_Pin, u32 Pin_State);

Input
----------
To do GPIO input test, the following steps are mandatory.

1. Select GPIO pin, and set GPIO mode to input.

   .. code:: c

      GPIO_InitStruct.GPIO_Pin = GPIO_Pin;
      GPIO_InitStruct.GPIO_Mode = GPIO_Mode_IN;

2. Initialize hardware using the parameters in step 1.

   .. code:: c

      GPIO_Init(GPIO_InitTypeDef *GPIO_InitStruct);

3. Read a specified output port pin.

   .. code:: c

      GPIO_ReadDataBit(u32 GPIO_Pin);

Interrupt
------------------
To do GPIO interrupt test, the following steps are mandatory.

1. Select GPIO pin, set GPIO pin mode to interrupt, no pull, and configure interrupt trigger type, polarity, debounce.

   .. code:: c

      GPIO_InitStruct.GPIO_Pin = GPIO_Pin;
      GPIO_InitStruct.GPIO_PuPd = GPIO_PuPd_NOPULL;
      GPIO_InitStruct.GPIO_Mode = GPIO_Mode_INT;
      GPIO_InitStruct.GPIO_ITTrigger = trigger_type;
      GPIO_InitStruct.GPIO_ITPolarity = polarity;
      GPIO_InitStruct.GPIO_ITDebounce=GPIO_INT_DEBOUNCE_ENABLE(or GPIO_INT_DEBOUNCE_DISABLE);

2. Initialize hardware using the parameters in step 1.

   .. code:: c

      GPIO_Init(GPIO_InitTypeDef *GPIO_InitStruct);

3. Register and enable the GPIO interrupt.

   .. code:: c

      InterruptRegister(GPIO_INTHandler,GPIO_DEV_TABLE[port].IrqNum, (u32)GPIO_DEV_TABLE[por t].GPIOx, 10);
      InterruptEn(GPIO_DEV_TABLE[port].IrqNum, 10);

4. (Optional) Configure the GPIO interrupt mode.

   .. code:: c

      GPIO_INTMode(u32 GPIO_Pin, u32 NewState, u32 GPIO_ITTrigger, u32 GPIO_ITPolarity, u32 GPIO_ITDebounce);

5. Register user handle.

   .. code:: c

      GPIO_UserRegIrq(GPIO_Pin, gpio_test_irq_handler, (&GPIO_InitStruct_Temp));

6. Enable the specified GPIO pin interrupt.

   .. code:: c

      GPIO_INTConfig(GPIO_Pin, ENABLE);
