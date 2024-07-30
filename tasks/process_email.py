#!/usr/bin/env python3

from robocorp import workitems


def process_letter():
    item = workitems.inputs.current
    return item.payload