"C:\Users\%USERNAME%\AppData\Local\Arduino15\packages\DxCore\tools\avr-gcc\7.3.0-atmel3.6.1-azduino7b1\bin\avr-gcc.exe" -x c -funsigned-char -funsigned-bitfields -DUARTTX=C0 -DWDTTIME=8 -DLED=D0 -D__AVR_AVR64DB64__ -DENTRYCOND_REQUIRE=0x34 -DLED_START_FLASHES=25 -DOTA_COPY=0 -DLED_INVERT  -I"../.."  -Os -ffixed-r20 -ffixed-r21 -ffunction-sections -fdata-sections -fpack-struct -fshort-enums -mrelax -g3 -Wall -Wextra -Werror -mmcu=avr64db64 -c -std=gnu11 -MD -MP -MF"bootloader.d" -MT"bootloader.d" -MT"bootloader.o"   -o "bootloader.o" "./optiboot_dx_mod.c" 


"C:\Users\%USERNAME%\AppData\Local\Arduino15\packages\DxCore\tools\avr-gcc\7.3.0-atmel3.6.1-azduino7b1\bin\avr-gcc.exe"  -o ./bootloader.elf  ./bootloader.o   -nostartfiles -nostdlib -Wl,-static -Wl,-Map="bootloader.map" -Wl,--start-group -Wl,-lm  -Wl,--end-group -mrelax -Wl,-section-start=.text=0x0 -Wl,-section-start=.application=0x200 -Wl,-section-start=.ota_copy=0x1c8 -Wl,-section-start=.spmtarg=0x1fa -Wl,-section-start=.version=0x1fe  -mmcu=avr64db64


"C:\Users\%USERNAME%\AppData\Local\Arduino15\packages\DxCore\tools\avr-gcc\7.3.0-atmel3.6.1-azduino7b1\bin\avr-objcopy.exe" -O ihex -R .eeprom -R .fuse -R .lock -R .signature -R .user_signatures  "bootloader.elf" "bootloader.hex"



"C:\Users\%USERNAME%\AppData\Local\Arduino15\packages\DxCore\tools\avr-gcc\7.3.0-atmel3.6.1-azduino7b1\bin\avr-objdump.exe" -h -S "bootloader.elf" > "bootloader.lss"


"C:\Users\%USERNAME%\AppData\Local\Arduino15\packages\DxCore\tools\avr-gcc\7.3.0-atmel3.6.1-azduino7b1\bin\avr-size.exe" "bootloader.elf"

cmd /k