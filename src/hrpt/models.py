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
This module contains the data objects used by hrpt
"""

import enum
from dataclasses import dataclass, field


class ParseError(ValueError):
    """Raised when a parser can not translate an incoming value to a standard value"""


class RenderError(ValueError):
    """Raised when a renderer encounters a situation is doesn't know how to render"""


class Mode(enum.Enum):
    """Enumeration of operating modes"""

    FM = "FM"
    NARROW_FM = "NFM"

class Band(enum.Enum):
    """Enum with extra data elements for all the radio bands"""
    def __new__(cls, *args, **kwds):
        #value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj
    def __init__(self, _, start_freq, end_freq):
        # can't set value from __init__, but the argument gets passed
        # so we have an unused argument here
        self.start_freq = start_freq
        self.end_freq = end_freq

    AMATEUR_2M = "2m", 144_000_000, 148_000_000
    AMATEUR_70CM = "70cm", 420_000_000, 450_000_000
    AMATEUR_1_25M = "1.25m", 222_000_000, 225_000_000
    GMRS = "GMRS", 462_000_000, 467_712_500
    MURS = "MURS", 151_820_000, 154_600_000
    NOAAWX = "NOAA Wx", 161_650_000, 162_550_000
    UNKNOWN = "unknown", 0, 0

class Frequency(int):
    """Subclass of int to store a Frequency in Hz"""

    @property
    def band(self):
        """Return the band the frequency is in"""
        for band in Band:
            if self >= band.start_freq and self <= band.end_freq:
                return band
        return Band.UNKNOWN

@dataclass
class Memory:
    """An internal representation of a single memory in a radio

    Based on CHIRP, since CHIRP's format is known to support dozens of radios

    You should not set both tx_ctcss_freq and tx_dcs_code

    You should not set both rx_ctcss_freq and rx_dcs_code
    """

    number: int
    frequency: "Frequency" = field(init=False, default=None)
    mode: "Mode" = field(init=False, default=Mode.FM)
    offset: int = field(init=False, default=None)
    tx_ctcss_freq: float = field(init=False, default=None)
    rx_ctcss_freq: float = field(init=False, default=None)
    tx_dcs_code: int = field(init=False, default=None)
    rx_dcs_code: int = field(init=False, default=None)
    name6: str = field(init=False, default=None)
    name8: str = field(init=False, default=None)
    name16: str = field(init=False, default=None)
    description: str = field(init=False, default=None)

    def frequency_in_mhz(self):
        "return frequency as a float in MHz"
        return self.frequency / 1_000_000

    def tx_ctcss_freq_in_khz(self):
        "return tx_tone_freq as a float in KHz"
        if self.tx_ctcss_freq:
            return self.tx_ctcss_freq / 1_000
        return self.tx_ctcss_freq

    def rx_ctcss_freq_in_khz(self):
        "return rx_tone_freq as a float in KHz"
        if self.rx_ctcss_freq:
            return self.rx_ctcss_freq / 1_000
        return self.rx_ctcss_freq
