#
# Copyright (c) 2024 Jared Crapo, K0TFU
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
This module contains a number of useful helper functions
"""


def standard_offset(frequency):
    """Calculate the standard offset for a given frequency

    Offset is returned as an integer in Hz, or 0 if this function isn't smart enough to
    calculate it
    """
    if not frequency:
        return 0

    if frequency >= 144_000_000 and frequency < 148_000_000:
        # 2m amateur radio band
        offset = 600_000
    elif frequency >= 222_000_000 and frequency < 225_000_000:
        # 1.25m amateur radio band
        offset = -1_600_000
    elif frequency >= 440_000_000 and frequency < 450_000_000:
        # 70cm amateur radio band
        offset = 5_000_000
    elif frequency >= 450_000_000 and frequency < 470_000_000:
        # UHF, GMRS falls in this range
        offset = 5_000_000
    else:
        # default
        offset = 600_000

    return offset


def frequency_step(frequency):
    """Calculate the standard frequency step for a given frequency"""
    ## TODO do this based on the band of the frequency
    step = 0

    if not frequency:
        return step

    if frequency >= 144_000_000 and frequency < 148_000_000:
        # 2m amateur radio band
        step = 5_000
    if frequency >= 151_000_000 and frequency < 155_000_000:
        # MURS
        step = 5_000
    if frequency >= 161_000_000 and frequency < 163_000_000:
        # NOAA Weather
        step = 25_000
    elif frequency >= 222_000_000 and frequency < 225_000_000:
        # 1.25m amateur radio band
        step = 10_000
    elif frequency >= 420_000_000 and frequency < 450_000_000:
        # 70cm amateur radio band
        step = 25_000
    elif frequency >= 462_000_000 and frequency < 468_000_000:
        # GMRS falls in this range
        step = 12_500
    else:
        step = 5_000

    return step
