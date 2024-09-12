.. _flash_layout:


This chapter introduces the default Flash layout of |CHIP_NAME| and how to modify the Flash layout if needed.

Introduction
------------------------
The default Flash layout used in SDK is illustrated in the following figure and table. The layout takes the 8MB Flash as an example. The start address of boot manifest is fixed to 0x0800_0000, and other start addresses can be configured by users flexibly.

.. figure:: ../figures/flash_layout.*
   :scale: 120%
   :align: center

   Flash layout


.. table:: Flash layout
   :width: 100%
   :widths: auto
   
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | Item                         | Physical address | Size (KB) | Description                                                                                           | Mandatory |
   +==============================+==================+===========+=======================================================================================================+===========+
   | KM4 Bootloader manifest      | 0x0800_0000      | 4         | KM4 bootloader manifest                                                                               | √         |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | KM4 Bootloader               | 0x0800_1000      | 76        | KM4 bootloader (code/data), containing KM4 bootloader IMG, mapped to the virtual address 0x0F80_0000. | √         |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | Key Certificate              | 0x0801_4000      | 4         | Public key hash information for other images.                                                         | √         |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | IMG2 manifest                | 0x0801_5000      | 4         | KM0 & KM4 Application & KM4 IMG3 manifest                                                             | √         |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | KM0 & KM4 Application        | 0x0801_6000      | 1912      | Combines KM0 image, KM4 image2 and KM4 image3 (if exists)                                             | √         |
   |                              |                  |           |                                                                                                       |           |
   |                              |                  |           | - KM0_IMG: KM0 image (code/data), mapped to the virtual address 0x0C00_0000.                          |           |
   |                              |                  |           |                                                                                                       |           |
   |                              |                  |           | - KM4_IMG2: KM4 non-secure image (code/data), mapped to the virtual address 0x0E00_0000.              |           |
   |                              |                  |           |                                                                                                       |           |
   |                              |                  |           | - KM4_IMG3\ :sup:`[1]`: secure image (code/data)                                                      |           |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | KM4 Bootloader manifest OTA2 | 0x0820_0000      | 4         | KM4 bootloader manifest                                                                               | √         |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | KM4 Bootloader OTA2          | 0x0820_1000      | 76        | KM4 bootloader (code/data), containing KM4 bootloader IMG, mapped to the virtual address 0x0F80_0000. | √         |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | Key Certificate OTA2         | 0x0821_4000      | 4         | Public key hash information for other images.                                                         | √         |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | IMG2 manifest OTA2           | 0x0821_5000      | 4         | KM0 & KM4 Application & KM4 IMG3 manifest                                                             | √         |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | KM0 & KM4 Application OTA2   | 0x0821_6000      | 1912      | Combines KM0 image, KM4 image2 and KM4 image3 (if exists)                                             | √         |
   |                              |                  |           |                                                                                                       |           |
   |                              |                  |           | - KM0_IMG: KM0 image (code/data), mapped to the virtual address 0x0C00_0000.                          |           |
   |                              |                  |           |                                                                                                       |           |
   |                              |                  |           | - KM4_IMG2: KM4 non-secure image (code/data), mapped to the virtual address 0x0E00_0000.              |           |
   |                              |                  |           |                                                                                                       |           |
   |                              |                  |           | - KM4_IMG3\ :sup:`[1]`: secure image (code/data)                                                      |           |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | FTL                          | 0x0870_0000      | 12        | For Bluetooth                                                                                         | ×         |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+
   | VFS                          | 0x0870_3000      | 128       | For file system                                                                                       | ×         |
   +------------------------------+------------------+-----------+-------------------------------------------------------------------------------------------------------+-----------+

.. note:: 

   [1] KM4_IMG3 only exists in the RTL8721Dx series.



Memory Management Unit (MMU)
--------------------------------------------------------
To achieve flexibility of image and for image encryption when RSIP is enabled (the fixed address is needed by IV when doing image encryption, refer to RSIP for more information), Flash MMU is applied by default. The default MMU layout used in SDK is illustrated in :ref:`flash_mmu_layout`.

.. figure:: ../figures/flash_mmu_layout.*
   :scale: 120%
   :align: center
   :name: flash_mmu_layout

   Flash MMU layout

How to Modify Flash Layout
----------------------------------------------------
The following locations in the Flash can be modified:

- Bootloader OTA2 location

- APP location

   - APP OTA1

   - APP OTA2

- FTL/VFS Location

Modifying Bootloader OTA2 Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The location of Bootloader OTA2 can be modified but requires 4KB alignment. The Bootloader OTA2 is disabled by default. If you want to enable Bootloader OTA2, shift the start address of Bootloader OTA2 right by 12 bits, then burn it to the OTP 0x36C~0x36D.


The method is to modify the address of ``IMG_BOOT_OTA2`` in ``{SDK}\component\soc\amebadplus\usrcfg\ameba_flashcfg.c``. After burning the Bootloader OTA2 into Flash through OTA, Boot ROM will decide whether to use Bootloader OTA1 or Bootloader OTA2 according to the version number.

.. code-block:: c
   :emphasize-lines: 10

   /*
   * @brif Flash layout is set according to Flash Layout in User Manual
   *  In each entry, the first item is flash region type, the second item is start address, the third item is end address */
   const FlashLayoutInfo_TypeDef Flash_Layout[] = {
       /*Region_Type,  [StartAddr, EndAddr]   */
       {IMG_BOOT,      0x08000000, 0x08013FFF}, //Boot Manifest(4K) + KM4 Bootloader(76K)
       //Users should modify below according to their own memory
       {IMG_APP_OTA1,  0x08014000, 0x081F3FFF}, //Certificate(4K) + Manifest(4K) + KR4 & KM4 Application OTA1 + Manifest(4K) + RDP IMG OTA1

       {IMG_BOOT_OTA2, 0x08200000, 0x08213FFF}, //Boot Manifest(4K) + KM4 Bootloader(76K) OTA
       {IMG_APP_OTA2,  0x08214000, 0x083F3FFF}, //Certificate(4K) + Manifest(4K) + KR4 & KM4 Application OTA2 + Manifest(4K) + RDP IMG OTA2
       {IMG_DSP,       0x08400000, 0x086FFFFF}, //Manifest(4K) + DSP IMG, only one DSP region in layout

       {FTL,           0x08700000, 0x08702FFF}, //FTL for BT(>=12K), The start offset of flash pages which is allocated to FTL physical map
       {VFS1,          0x08703000, 0x08722FFF}, //VFS region 1 (128K)
       {USER,          0xFFFFFFFF, 0xFFFFFFFF}, //reserve for user

       /* End */
       {0xFF,          0xFFFFFFFF, 0xFFFFFFFF},
   };


If the anti-rollback function is enabled to ensure that the version of the Bootloader can only be incrementing but cannot be rolled back, the version of the Bootloader needs to be changed before compiling. That is, ``IMG_VER`` in ``{SDK}\amebadplus_gcc_project\manifest.json`` needs to be modified.

.. code-block:: c
   :emphasize-lines: 6,7

	"MANIFEST_VER": 1,
	
	"boot":
	{
		"IMG_ID": "0",
		"IMG_VER_MAJOR": 1,
		"IMG_VER_MINOR": 1,

		"SEC_EPOCH": 1,
		
		"HASH_ALG": "sha256",
		
		"RSIP_IV": "01020304050607080000000000000000",
	},


.. note:: The location of Bootloader OTA1 is fixed to 0x0800_0000, and cannot be modified.


Modifying APP Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _flash_layout_app_ota1:

APP OTA1
^^^^^^^^^^^^^^^^
Follow the steps to modify the location of APP OTA1:

1. Modify the address of ``IMG_APP_OTA1`` in ``{SDK}\component\soc\amebadplus\usrcfg\ameba_flashcfg.c``.
   
   .. code-block:: c
      :emphasize-lines: 5

      const FlashLayoutInfo_TypeDef Flash_Layout[] = {
          /*Region_Type,  [StartAddr, EndAddr]   */
          {IMG_BOOT,      0x08000000, 0x08013FFF}, //Boot Manifest(4K) + KM4 Bootloader(76K)
          //Users should modify below according to their own memory
          {IMG_APP_OTA1,  0x08014000, 0x081F3FFF}, //Certificate(4K) + Manifest(4K) + KM4 Application OTA1 + Manifest(4K) + RDP IMG OTA1

          {IMG_BOOT_OTA2, 0x08200000, 0x08213FFF}, //Boot Manifest(4K) + KM4 Bootloader(76K) OTA
          {IMG_APP_OTA2,  0x08214000, 0x083F3FFF}, //Certificate(4K) + Manifest(4K) + KM4 Application OTA2 + Manifest(4K) + RDP IMG OTA2

          {FTL,           0x08700000, 0x08702FFF}, //FTL for BT(>=12K), The start offset of flash pages which is allocated to FTL physical map
          {VFS1,          0x08703000, 0x08722FFF}, //VFS region 1 (128K)
          {USER,          0xFFFFFFFF, 0xFFFFFFFF}, //reserve for user

          /* End */
          {0xFF,          0xFFFFFFFF, 0xFFFFFFFF},
      };


.. _flash_layout_app_ota1_step2:

2. Re-build the project to generate the Bootloader and APP OTA1.

.. _flash_layout_app_ota1_step3:

3. Modify the address of ``km0_km4_app.bin`` if you update the location of APP OTA1 through ImageTool, and download the new Bootloader and APP OTA1.

   .. figure:: ../figures/app_ota1_step3.png
      :scale: 50%
      :align: center


After that, Bootloader will load the image from the new location of APP OTA1 if the version of APP OTA1 is bigger.

APP OTA2
^^^^^^^^^^^^^^^^
1. Modify the address of ``IMG_APP_OTA2`` in ``{SDK}\component\soc\amebadplus\usrcfg\ameba_flashcfg.c``.

2. Re-build and download the new Bootloader and APP OTA2 as described in section :ref:`flash_layout_app_ota1` step :ref:`2 <flash_layout_app_ota1_step2>` ~ :ref:`3 <flash_layout_app_ota1_step3>`.

   .. code-block:: c

      /*
      * @brif Flash layout is set according to Flash Layout in User Manual
      *  In each entry, the first item is flash region type, the second item is start address, the third item is end address */
      const FlashLayoutInfo_TypeDef Flash_Layout[] = {
          /*Region_Type,  [StartAddr, EndAddr]   */
          {IMG_BOOT,      0x08000000, 0x08013FFF}, //Boot Manifest(4K) + KM4 Bootloader(76K)
          //Users should modify below according to their own memory
          {IMG_APP_OTA1,  0x08014000, 0x081F3FFF}, //Certificate(4K) + Manifest(4K) + KR4 & KM4 Application OTA1 + Manifest(4K) + RDP IMG OTA1

          {IMG_BOOT_OTA2, 0x08200000, 0x08213FFF}, //Boot Manifest(4K) + KM4 Bootloader(76K) OTA
          {IMG_APP_OTA2,  0x08214000, 0x083F3FFF}, //Certificate(4K) + Manifest(4K) + KR4 & KM4 Application OTA2 + Manifest(4K) + RDP IMG OTA2
          {IMG_DSP,       0x08400000, 0x086FFFFF}, //Manifest(4K) + DSP IMG, only one DSP region in layout

          {FTL,           0x08700000, 0x08702FFF}, //FTL for BT(>=12K), The start offset of flash pages which is allocated to FTL physical map
          {VFS1,          0x08703000, 0x08722FFF}, //VFS region 1 (128K)
          {USER,          0xFFFFFFFF, 0xFFFFFFFF}, //reserve for user

          /* End */
          {0xFF,          0xFFFFFFFF, 0xFFFFFFFF},
      };

After burning the APP OTA2 into Flash through OTA, Bootloader will load the image from the new location of APP OTA2 if the version of APP OTA2 is bigger.

Modifying FTL/VFS Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Modify the addresses of FTL and VFS1 in ``{SDK}\component\soc\amebadplus\usrcfg\ameba_flashcfg.c``.

2. Update the application image.

   .. code-block:: c
      :emphasize-lines: 14,15

      /*
      * @brif Flash layout is set according to Flash Layout in User Manual
      *  In each entry, the first item is flash region type, the second item is start address, the third item is end address */
      const FlashLayoutInfo_TypeDef Flash_Layout[] = {
          /*Region_Type,  [StartAddr, EndAddr]   */
          {IMG_BOOT,      0x08000000, 0x08013FFF}, //Boot Manifest(4K) + KM4 Bootloader(76K)
          //Users should modify below according to their own memory
          {IMG_APP_OTA1,  0x08014000, 0x081F3FFF}, //Certificate(4K) + Manifest(4K) + KR4 & KM4 Application OTA1 + Manifest(4K) + RDP IMG OTA1

          {IMG_BOOT_OTA2, 0x08200000, 0x08213FFF}, //Boot Manifest(4K) + KM4 Bootloader(76K) OTA
          {IMG_APP_OTA2,  0x08214000, 0x083F3FFF}, //Certificate(4K) + Manifest(4K) + KR4 & KM4 Application OTA2 + Manifest(4K) + RDP IMG OTA2
          {IMG_DSP,       0x08400000, 0x086FFFFF}, //Manifest(4K) + DSP IMG, only one DSP region in layout

          {FTL,           0x08700000, 0x08702FFF}, //FTL for BT(>=12K), The start offset of flash pages which is allocated to FTL physical map
          {VFS1,          0x08703000, 0x08722FFF}, //VFS region 1 (128K)
          {USER,          0xFFFFFFFF, 0xFFFFFFFF}, //reserve for user

          /* End */
          {0xFF,          0xFFFFFFFF, 0xFFFFFFFF},
      };

Flash Protect Enable
----------------------------------------
Before loading APP IMG, the Bootloader will read the Status Register from Flash. If only Quad Enable (QE) Bit is set in the output of bitwise AND between Status Register of Flash and status_mask in Flash_AVL (``{SDK}\component\soc\amebadplus\usrcfg\ameba_flashcfg.c``), do nothing, or the output of bitwise AND will be written to the Flash Status Register.

.. note::
   By default, setting the QE bit will unlock all the Block Protect Bits. To avoid this operation, set Block Protect bits corresponding to ``Status_mask`` in ``Flash_AVL`` to 0. For example, change the ``Status_mask`` of Winbond in the ``Flash_AVL`` to 0x000043C0.

.. figure:: ../figures/flash_protect_enable.*
   :scale: 60%
   :align: center

In order to avoid the image being damaged due to improper operation when using LittleFS to write user data, it is recommended to modify the location of FTL/LittleFS to the last 64KB area of Flash, and set the Block Protect Bit in the Status Register of Flash at the same time.

.. note::
   
      - Only the last 64KB area of Flash can be modified, and the other areas are protected. Remember to unlock the Flash during OTA upgrade, and keep it locked when OTA is completed.

      - For some Flashes, you cannot set the Flash to allow only the last block to be modified through Block Protect Bit. In this case, it is recommended to enable the Flash block protection of the first half part.


