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
    Band,
    Frequency,
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
        * channel 1 must not be empty
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

        # generate numbers 1 to 999, each of these lines must be present in the file
        # or ADMS-16 will refuse to import it
        for line_number in range(1, 1000):
            # special case to ensure we have a row in the file for channel 1
            # ADMS-16 won't import if there isn't a memory on channel 1
            if line_number == 1 and (not memories or memories[0].number != 1):
                call = Memory(number=1)
                call.frequency = Frequency(146_520_000)
                fileobj.write(f"{self.render_memory(call)}\n")
                continue

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
        if memory.mode == Mode.FM:
            narrow = "OFF"
            out.append("FM")
        elif memory.mode == Mode.NARROW_FM:
            narrow = "ON"
            out.append("FM")
        else:
            narrow = "OFF"
            # TODO, make this more robust for AM
            out.append(memory.mode.value)

        # column 7: digital/analog
        # could be AMS if you want to do auto CFM detection and switching
        out.append("FM")

        # column 8: name
        if memory.name16:
            out.append(f"{memory.name16}")
        else:
            out.append("")

        # columns 9, 10, 11: tone type, ctcss freq, dcs code
        (tone_type, ctcss_freq, dcs_code) = self.render_tone()
        out.append(tone_type)
        out.append(ctcss_freq)
        out.append(dcs_code)

        # column 12: User CTCSS
        out.append("1500 Hz")

        # column 13: RX DG-ID
        if memory.frequency.band in [Band.AMATEUR_1_25M]:
            out.append("-")
        else:
            out.append("RX 00")

        # column 14: TX DG-IG
        if memory.frequency.band in [Band.AMATEUR_1_25M]:
            # no idea why, but just figured this out from observation and testing
            out.append("-")
        else:
            out.append("TX 00")

        # column 15: Tx Power
        out.append("HIGH")

        # column 16: Scan
        out.append("YES")

        # column 17: step
        out.append(self.render_frequency_step(memory.frequency.band.tuning_step))

        # column 18: narrow
        out.append(narrow)

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
        return f"{mhz:.5f}"

    def render_offset_as_mhz(self, offset):
        """render the offset frequency as a string in MHz
        gotta take the abs of the frequency to comply with the file format expectations
        """
        mhz = abs(offset) / 1_000_000
        return f"{mhz:.5f}"

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
            f" offset_frequency of '{offset_freq}'"
        )

    def render_tone(self):
        """render tone type, ctcss freq, and dtcs code

        use self._memory
        """
        # if we have a ctcss tone, that takes precendence
        if self._memory.tx_ctcss_freq:
            tone_type = "TONE"
            ctcss_freq = self.render_ctcss_freq(self._memory.tx_ctcss_freq)
            dcs_code = self.render_dcs_code(None)
        elif self._memory.tx_dcs_code:
            tone_type = "DCS"
            ctcss_freq = self.render_ctcss_freq(None)
            dcs_code = self.render_dcs_code(self._memory.tx_dcs_code)
        else:
            tone_type = "OFF"
            ctcss_freq = self.render_ctcss_freq(None)
            dcs_code = self.render_dcs_code(None)

        return (tone_type, ctcss_freq, dcs_code)

    def render_ctcss_freq(self, tone_freq):
        """Render a ctcss tone frequency"""
        if not tone_freq:
            # default tone_freq
            tone_freq = 100
        return f"{tone_freq:.1f} Hz"

    def render_dcs_code(self, dcs_code):
        """Render a dcs code as a string left padded with zeros"""
        if not dcs_code:
            # default dcs_code
            dcs_code = 23
        return f"{dcs_code:03}"

    def render_frequency_step(self, step):
        """Render a frequency step as a string"""
        step = step / 1_000
        return f"{step:.1f}KHz"
