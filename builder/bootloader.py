# Copyright 2019-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from os.path import isfile, join

from SCons.Script import Import, Return

Import("env")

board = env.BoardConfig()
platform = env.PioPlatform()
FRAMEWORK_DIR = platform.get_package_dir(
    platform.frameworks[env.get("PIOFRAMEWORK")[0]]['package'])


def get_suitable_optiboot_binary(board_config):
    mcu = board_config.get("build.mcu", "").lower()
    f_cpu = board_config.get("build.f_cpu", "16000000L").upper()
    uart = board_config.get("hardware.uart", "uart0").upper()
    bootloader_file = "optiboot_flash_%s_%s_%s_%s.hex" % (
        mcu, uart, env.subst("$UPLOAD_SPEED"), f_cpu)
    bootloader_path = join(FRAMEWORK_DIR, "bootloaders", "optiboot_flash",
        "bootloaders", "%s" % mcu, "%s" % f_cpu, bootloader_file)
    if isfile(bootloader_path):
        return bootloader_path

    return bootloader_path.replace(".hex", "_BIGBOOT.hex")


common_flags = [
    "avrdude", "-p", "$BOARD_MCU", "-C",
    join(platform.get_package_dir("tool-avrdude"), "avrdude.conf"),
    "-c", "$UPLOAD_PROTOCOL", "$UPLOAD_FLAGS"
]

# Common for all bootloaders
lock_bits = board.get("bootloader.lock_bits", "0x0F")
unlock_bits = board.get("bootloader.unlock_bits", "0x3F")
bootloader_path = board.get("bootloader.file", "")

if board.get("build.core", "") in ("MiniCore", "MegaCore", "MightyCore"):
    if not isfile(bootloader_path):
        bootloader_path = get_suitable_optiboot_binary(board)
    fuses_action = env.SConscript("fuses.py", exports="env")
else:
    if not isfile(bootloader_path):
        bootloader_path = join(FRAMEWORK_DIR, "bootloaders", bootloader_path)

    if not board.get("bootloader", {}):
        sys.stderr.write(
            "Error: missing bootloader configuration!\n")
        env.Exit(1)


    lfuse = board.get("bootloader.low_fuses", "")
    hfuse = board.get("bootloader.high_fuses", "")
    efuse = board.get("bootloader.extended_fuses", "")

    if not all(f for f in (lfuse, hfuse)):
        sys.stderr.write(
            "Error: Missing bootloader fuses!\n")
        env.Exit(1)

    fuses_cmd = [
        "-Ulock:w:%s:m" % unlock_bits,
        "-Uhfuse:w:%s:m" % hfuse,
        "-Ulfuse:w:%s:m" % lfuse
    ]

    if efuse:
        fuses_cmd.append("-Uefuse:w:%s:m" % efuse)

    fuses_action = env.VerboseAction(
        " ".join(common_flags + fuses_cmd), "Setting fuses")

if not isfile(bootloader_path):
    sys.stderr.write("Error: Couldn't find file %s\n" % bootloader_path)
    env.Exit(1)

bootloader_flags = [
    "-e", '-Uflash:w:"%s":i' % bootloader_path, "-Ulock:w:%s:m" % lock_bits]

bootloader_actions = [
    fuses_action,
    env.VerboseAction(" ".join(common_flags + bootloader_flags),
                      "Uploading bootloader")
]

Return("bootloader_actions")
