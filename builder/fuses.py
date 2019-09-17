Import("env")


def get_lfuse(mcu, f_cpu, oscillator, bod, eesave):
    mcus_1 = (
        "atmega2561", "atmega2560", "atmega1284", "atmega1284p", "atmega1281",
        "atmega1280", "atmega644a", "atmega644p", "atmega640", "atmega328",
        "atmega328p", "atmega324a", "atmega324p", "atmega324pa", "atmega168",
        "atmega168p", "atmega164a", "atmega164p", "atmega88", "atmega88p",
        "atmega48", "atmega48p")

    mcus_2 = (
        "atmega328pb", "atmega324pb", "atmega168pb", "atmega162", "atmega88pb",
        "atmega48pb", "at90can128", "at90can64", "at90can32")

    mcus_3 = ("atmega8535", "atmega8515", "atmega32", "atmega16", "atmega8")

    mcus_4 = ("attiny13", "attiny13a")

    if mcu in mcus_1:
        if oscillator == "external":
            return 0xf7
        else:
            return 0xe2 if f_cpu == "8000000L" else 0x62

    elif mcu in mcus_2:
        if oscillator == "external":
            return 0xff
        else:
            return 0xe2 if f_cpu == "8000000L" else 0x62

    elif mcu in mcus_3:
        if bod == "4.0v":
            bod_bits = 0b11
        elif bod == "2.7v":
            bod_bits = 0b01
        else:
            bod_bits = 0b00

        bod_offset = bod_bits << 6
        if oscillator == "external":
            return 0xff & ~ bod_offset
        else:
            if f_cpu == "8000000L":
                return 0xe4 & ~ bod_offset
            else:
                return 0xe1 & ~ bod_offset

    elif mcu in mcus_4:
        eesave_bit = 1 if eesave == "yes" else 0
        eesave_offset = eesave_bit << 6
        if oscillator == "external":
            return 0x78 & ~ eesave_offset
        else:
            if f_cpu == "9600000L":
                return 0x7a & ~ eesave_offset
            elif f_cpu == "4800000L":
                return 0x79 & ~ eesave_offset
            elif f_cpu == "1200000L":
                return 0x6a & ~ eesave_offset
            elif f_cpu == "600000L":
                return 0x69 & ~ eesave_offset
            elif f_cpu == "128000L":
                return 0x7b & ~ eesave_offset
            elif f_cpu == "16000L":
                return 0x6b & ~ eesave_offset

    else:
        print("Error: Couldn't calculate lfuse for %s" % mcu)
        env.Exit(1)


def get_hfuse(mcu, uart, oscillator, bod, eesave):
    mcus_1 = (
        "atmega2561", "atmega2560", "atmega1284", "atmega1284p",
        "atmega1281", "atmega1280", "atmega644a", "atmega644p",
        "atmega640", "atmega328", "atmega328p", "atmega328pb",
        "atmega324a", "atmega324p", "atmega324pa", "atmega324pb",
        "at90can128", "at90can64", "at90can32")

    mcus_2 = ("atmega164a", "atmega164p", "atmega162")

    mcus_3 = (
        "atmega168", "atmega168p", "atmega168pb", "atmega88", "atmega88p",
        "atmega88pb", "atmega48", "atmega48p", "atmega48pb")

    mcus_4 = ("atmega128", "atmega64", "atmega32")

    mcus_5 = ("atmega8535", "atmega8515", "atmega16", "atmega8")

    mcus_6 = ("attiny13", "attiny13a")

    eesave_bit = 1 if eesave == "yes" else 0
    eesave_offset = eesave_bit << 3
    ckopt_bit = 1 if oscillator == "external" else 0
    ckopt_offset = ckopt_bit << 4
    if mcu in mcus_1:
        if uart == "no_bootloader":
            return 0xdf & ~ eesave_offset
        else:
            return 0xde & ~ eesave_offset
    elif mcu in mcus_2:
        if uart == "no_bootloader":
            return 0xdd & ~ eesave_offset
        else:
            return 0xdc & ~ eesave_offset
    elif mcu in mcus_3:
        if bod == "4.3v":
            return 0xdc & ~ eesave_offset
        elif bod == "2.7v":
            return 0xdd & ~ eesave_offset
        elif bod == "1.8v":
            return 0xde & ~ eesave_offset
        else:
            return 0xdf & ~ eesave_offset
    elif mcu in mcus_4:
        if uart == "no_bootloader":
            return (0xdf & ~ ckopt_offset) & ~ eesave_offset
        else:
            return (0xde & ~ ckopt_offset) & ~ eesave_offset
    elif mcu in mcus_5:
        if uart == "no_bootloader":
            return (0xdd & ~ ckopt_offset) & ~ eesave_offset
        else:
            return (0xdc & ~ ckopt_offset) & ~ eesave_offset
    elif mcu in mcus_6:
        if bod == "4.3v":
            return 0x9
        elif bod == "2.7v":
            return 0xfb
        elif bod == "1.8v":
            return 0xfd
        else:
            return 0xff

    else:
        print("Error: Couldn't calculate hfuse for %s" % mcu)
        env.Exit(1)


def get_efuse(mcu, uart, bod):

    mcus_1 = (
        "atmega2561", "atmega2560", "atmega1284", "atmega1284p",
        "atmega1281", "atmega1280", "atmega644a", "atmega644p",
        "atmega640", "atmega328", "atmega328p", "atmega324a",
        "atmega324p", "atmega324pa", "atmega164a", "atmega164p")

    mcus_2 = ("atmega328pb", "atmega324pb")

    mcus_3 = (
        "atmega168", "atmega168p", "atmega168pb", "atmega88",
        "atmega88p", "atmega88pb")

    mcus_4 = ("atmega128", "atmega64", "atmega48", "atmega48p")

    mcus_5 = ("at90can128", "at90can64", "at90can32")

    if mcu in mcus_1:
        if bod == "4.3v":
            return 0xfc
        elif bod == "2.7v":
            return 0xfd
        elif bod == "1.8v":
            return 0xfe
        else:
            return 0xff

    elif mcu in mcus_2:
        if bod == "4.3v":
            return 0xf4
        elif bod == "2.7v":
            return 0xf5
        elif bod == "1.8v":
            return 0xf6
        else:
            return 0xf7

    elif mcu in mcus_3:
        return 0xfd if uart == "no_bootloader" else 0xfc

    elif mcu in mcus_4:
        return 0xff

    elif mcu in mcus_5:
        if bod == "4.1v":
            return 0xfd
        elif bod == "4.0v":
            return 0xfb
        elif bod == "3.9v":
            return 0xf9
        elif bod == "3.8v":
            return 0xf7
        elif bod == "2.7v":
            return 0xf5
        elif bod == "2.6v":
            return 0xf3
        elif bod == "2.5v":
            return 0xf1
        else:
            return 0xff

    else:
        print("Error: Couldn't calculate efuse for %s" % mcu)
        env.Exit(1)


board = env.BoardConfig()
mcu = board.get("build.mcu", "").lower()
f_cpu = board.get("build.f_cpu", "16000000L").upper()
oscillator = board.get("hardware.oscillator", "external").lower()
bod = board.get("hardware.bod", "2.7v").lower()
uart = board.get("hardware.uart", "uart0").lower()
eesave = board.get("hardware.eesave", "yes").lower()

print("Target configuration:")
print("Clock speed = %s, Oscillator = %s, BOD level = %s, UART port = %s, Save EEPROM = %s" % (
    f_cpu, oscillator, bod, uart, eesave))

lfuse = board.get("fuses.lfuse") if board.get("fuses.lfuse", "") else hex(
    get_lfuse(mcu, f_cpu, oscillator, bod, eesave))
hfuse = board.get("fuses.hfuse") if board.get("fuses.hfuse", "") else hex(
    get_hfuse(mcu, uart, oscillator, bod, eesave))
efuse = board.get("fuses.efuse") if board.get("fuses.efuse", "") else hex(
    get_efuse(mcu, uart, bod))
lock = board.get("fuses.lock", "0x3f")

print("Calculated fuses: [lock = %s, lfuse = %s, hfuse = %s, efuse = %s]" % (
    lock, lfuse, hfuse, efuse))

env.Replace(FUSESCMD=" ".join(["avrdude", "$UPLOADERFLAGS"] + [
    "-Ulock:w:%s:m" % lock,
    "-Uefuse:w:%s:m" % efuse,
    "-Uhfuse:w:%s:m" % hfuse,
    "-Ulfuse:w:%s:m" % lfuse
]))
