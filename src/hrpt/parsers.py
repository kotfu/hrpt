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
This module contains all parser classes for the incoming file formats
"""

import csv

from .models import (
    Frequency,
    Memory,
    Mode,
    ParseError,
)


class CHIRPParser:
    """A class to parse CHIRP CSV exports

    [CHIRP](https://chirpmyradio.com/projects/chirp/wiki/Home) can program
    dozens of handheld VHF/UHF radios. Mostly it programs memory channels, but
    for some radios it can do other settings too. CHIRP can export memories to
    a comma separated value file.

    This file has the following characteristics:
        * comma separated values, no quotes on values
        * cr/lf line endings
        * 1 header line with column names
        * 1 row per saved memory, empty memories do not have a row

    """
    def __init__(self):
        super().__init__()
        self.line_number = 0

    def parse(self, fileobj):
        """Parse a CHIRP CSV export into a list of Memory objects"""
        memories = []
        reader = csv.reader(fileobj)
        # discard the header row
        self.line_number += 1
        _ = next(reader)
        # iterate through the rest of the file
        for row in reader:
            self.line_number += 1
            # row contains a list of strings
            number = self.translate_number(row[0])
            m = Memory(number)
            m.frequency = self.translate_frequency(row[2])
            m.mode = self.translate_mode(row[12])
            m.offset = self.translate_offset(row[3], row[4])
            self.parse_squelch(row, m)
            m.name16 = row[1]
            memories.append(m)

        return memories

    def parse_squelch(self, row, memory):
        """Parse and set the CTCSS and DCS squelch"""
        if row[5] == "Tone":
            memory.tx_ctcss_freq = self.translate_ctcss(row[6])
        if row[5] == "DTCS":
            memory.tx_dcs_code = self.translate_dcs(row[8])

    def translate_number(self, value):
        """Translate memory number from a string to an integer"""
        return int(value)

    def translate_frequency(self, value):
        """Translate frequency from a string to a Frequency"""
        return Frequency(int(float(value) * 1_000_000))

    def translate_mode(self, value):
        """Translate the mode to the proper enum"""
        if value == Mode.FM.value:
            return Mode.FM
        elif value == Mode.NARROW_FM.value:
            return Mode.NARROW_FM
        raise ParseError("Unknown Mode '{value}' on line {self.line_number}")

    def translate_offset(self, direction, value):
        """Create the offset from two string fields"""
        if direction == "+" and value:
            # positive offset, turn value into an integer in Hz
            return int(float(value) * 1_000_000)
        if direction == "-" and value:
            # negative offset, turn value into a negative integer in Hz
            return int(float(value) * 1_000_000) * -1
        return 0

    def translate_ctcss(self, value):
        """CHIRP stores CTCSS tones as strings in Hz, we store float of Hz"""
        return float(value)

    def translate_dcs(self, value):
        """CHIRP stores DCS codes as string, we store them as integers"""
        return int(value)
