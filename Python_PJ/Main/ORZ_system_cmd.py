# -*- coding: utf-8 -*-
import os
from ORZ_exception import *

def sys_write(cmd):
    """
    open pipe to execute system call
    """
    x = os.popen(cmd)
    result = x.readlines()
    x.close()
    return result


def sys_read(dl, x):
    """
    check string x(string) in dl(list object)
    sys_write& sys_read should couple-pair program
    """
    if any(x in s for s in dl):
        print("match")
    else:
        print("miss!")
        raise ORZ_SystemFail


if __name__ == "__main__":
    r = sys_write("dir/w")
    sys_read(r, "GUI_Main")
    try:
        sys_read(r, "ooxx")
    except ORZ_SystemFail:
        print("got cmd fail")
