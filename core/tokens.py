import binascii
import os


def rand(args) -> str:
    return "0x" + binascii.b2a_hex(os.urandom(int(args[0]))).decode("ascii")


def minit(args) -> str:
    result = ""

    for i in range(int(args[0])):
        address = 0x60 + (i * 0x20)
        result += "PUSH32 0x" + binascii.b2a_hex(os.urandom(32)).decode("ascii") + "\n"
        result += "PUSH32 " + hex(address) + "\n"
        result += "MSTORE\n"

    return result
