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
This module contains all render classes for output file formats
"""

from .helpers import (
    standard_offset,
)
from .models import (
    Memory,
    Mode,
    RenderError,
)


class ADMS16Renderer:
    """Render output for ADMS-16, the software from Yaesu for the FRM-500DR/DE

    The file format is a CSV file with the following characteristics:
        * comma separated values, no quotes on values
        * lf line endings
        * no header lines
        * 999 rows, numbered 1 to 999. Empty memories must be represented as a row
          in the file or ADMS-16 will not load the file
    """

    def __init__(self):
        super().__init__()
        self._memory = None

    def render(self, memories, fileobj):
        """Render a list of memories to the file object

        fileobj needs to be opened with newline = '\n'

        """
        # TODO memories must be sorted in increasing order of memory number
        # and be unique memory numbers
        #
        # lineno is the line number in the file, which must have 999 lines when
        # we are done
        #
        # memory_pos is the index in memories that we are currently iterating on
        memory_pos = 0

        for line_number in range(1, 999):
            if memories[memory_pos].number == line_number:
                fileobj.write(f"{self.render_memory(memories[memory_pos])}\n")
                # increment memory_pos to point to the next spot in the array,
                # unless we are already at the end
                if memory_pos + 1 < len(memories):
                    memory_pos += 1
            else:
                empty = Memory(number=line_number)
                fileobj.write(f"{self.render_memory(empty)}\n")
                # no need to increment memory_pos because we didn't use
                # a memory, we just put a blank line

    def render_memory(self, memory):
        """generate a representing one memory, which will be one line in the file"""
        # save memory in self._memory so we can use it for error reporting
        self._memory = memory
        if memory.number and not memory.frequency:
            # this is an empty memory
            return f"{memory.number},,,,,,,,,,,,,,,,,,,,0"

        # build an array of strings, one elements for each column in the output
        out = []
        # column 1: memory number
        out.append(f"{memory.number}")

        # column 2: rx frequency
        if not memory.frequency:
            raise RenderError("Memory '{memory.number}' does not have a frequency.")
        out.append(self.render_frequency_as_mhz(memory.frequency))

        # columns 3, 4, 5: tx frequency, offset, offset direction
        if memory.offset:
            # we have an offset, apply it to the tx frequency
            tx_freq = memory.frequency + memory.offset
            out.append(self.render_frequency_as_mhz(tx_freq))
            out.append(self.render_offset_as_mhz(memory.offset))
            out.append(self.render_offset_direction(memory.offset))
        else:
            # no offset, so it's a simplex frequency, tx freq is the same as rx freq
            out.append(self.render_frequency_as_mhz(memory.frequency))
            # even though we don't have an offset, this file format requires one,
            # pick one based on the frequency
            out.append(self.render_offset_as_mhz(standard_offset(memory.frequency)))
            out.append(self.render_offset_direction(memory.offset))

        # column 6: mode
        out.append(memory.mode.value)

        # column 7: digital/analog
        # could be AMS if you want to do auto CFM detection and switching
        out.append("FM")

        # column 8: name
        out.append(f"{memory.name16}")

        # column 9: tone
        out.append(self.render_ctcss_freq(memory.tx_ctcss_freq))

        # column 10: ctcss freq
        out.append("placeholder")

        # column 11: dtcs code
        out.append("placeholder")

        # column 12: User CTCSS
        out.append("1500 Hz")

        # column 13: RX DG-ID
        out.append("RX 00")

        # column 14: TX DG-IG
        out.append("TX 00")

        # column 15: Tx Power
        out.append("HIGH")

        # column 16: Scan
        out.append("YES")

        # column 17: step
        out.append("placeholder")

        # column 18: narrow
        # default could be OFF unless we know its narrow FM
        out.append("placeholder")

        # column 19: clock shift
        out.append("OFF")

        # column 20: comment
        out.append("")

        # column 21: last
        out.append("0")

        return ",".join(out)

    def render_frequency_as_mhz(self, freq):
        """render an integer frequency in hz as mhz"""
        mhz = freq / 1_000_000
        return f"{mhz:.4f}"

    def render_offset_as_mhz(self, offset):
        """render the offset frequency as a string in MHz
        gotta take the abs of the frequency to comply with the file format expectations
        """
        mhz = abs(offset) / 1_000_000
        return f"{mhz:.2f}"

    def render_offset_direction(self, offset_freq):
        """take an integer offset frequency and turn it into the proper string"""
        if not offset_freq:
            return "OFF"
        elif offset_freq < 0:
            return "-RPT"
        elif offset_freq > 0:
            return "+RPT"
        # shouldn't get here
        raise RenderError(
            f"Memory '{self._memory.number}' has an unknown"
            f" offset_frequency of '{offset_freq}'")

    def render_ctcss_freq(self, tone_freq):
        """Render a ctcss tone frequency"""
        if not tone_freq:
            tone_freq = 100
        return f"{tone_freq:.1f} Hz"
