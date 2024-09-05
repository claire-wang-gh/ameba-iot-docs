.. _pinctrl:

Usage
------------------------

To configure the pin multiplexing function, follow the steps below:

1. Turn off the SWD or enable audio pad share if the pin default function is SWD or audio, and configure it to other functions.
   
   .. code-block:: C

      Pinmux_Swdoff();
      HAL_WRITE32(PINMUX_REG_BASE, REG_PAD_AUD_PAD_CTRL, 0x1FFFFF);

2. Turn off the SWD if the pin default function is SWD, and configure it to other functions.

   .. code-block:: C

      Pinmux_Swdoff();

3. Configure pinmux function.

   .. code-block:: C

      Pinmux_Config(u8 PinName, u32 PinFunc);

4. Set pin pull type.

   .. code-block:: C

      PAD_PullCtrl(u8 PinName, u8 PullType); //normal mode
      PAD_SleepPullCtrl(u8 PinName, u8 PullType); //sleep and deep-sleep mode

5. Set driving strength if needed.

   .. code-block:: C

      PAD_DrvStrength(u8 PinName, u32 DrvStrength);
