#!/usr/bin/env python
"""
test.py

Copyright (c) Weipeng He <weipeng.he@idiap.ch>
"""

from play_by_ear import PlayByEar, CLI

def main():
    pbe = PlayByEar(CLI())
    pbe.run()

if __name__ == "__main__":
    main()

# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

