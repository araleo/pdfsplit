import os
import sys
from pathlib import Path

from mensagens import TEXTO_ARGV


def sanitize_input():
    verify_args_num()
    size_or_parts = size_or_parts_to_int()
    path = verify_out_dir()
    mode = verify_split_mode()
    return size_or_parts, path, mode


def verify_args_num():
    if len(sys.argv) != 4:
        print(TEXTO_ARGV)
        exit()


def size_or_parts_to_int():
    try:
        size_or_parts = int(sys.argv[1])
    except ValueError:
        print(TEXTO_ARGV)
        exit()
    else:
        if size_or_parts <= 0:
            print(TEXTO_ARGV)
            exit()
        return size_or_parts


def verify_out_dir():
    path = sys.argv[2]
    if not os.path.exists(Path(os.path.abspath(path))):
        print(TEXTO_ARGV)
        exit()
    return path


def verify_split_mode():
    mode = sys.argv[3]
    if mode != "tamanho" and mode != "partes":
        print(TEXTO_ARGV)
        exit()
    return mode

