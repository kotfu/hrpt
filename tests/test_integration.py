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

import filecmp

import hrpt


def test_CHIRP_to_ADMS16(input_files_dir, output_files_dir, tmp_path):
    input_file = input_files_dir / "mem1000-CHIRP.csv"
    parser = hrpt.parsers.CHIRPParser()
    with open(input_file, encoding="utf8", newline='') as fileobj:
        memories = parser.parse(fileobj)

    reference_file = output_files_dir / "mem1000-ADMS16.csv"
    test_output_file = tmp_path / "CHIRP-to-ADMS16.csv"
    renderer = hrpt.renderers.ADMS16Renderer()
    with open(test_output_file, mode="w", encoding="utf8", newline="\n") as fileobj:
        renderer.render(memories, fileobj)

    assert filecmp.cmp(reference_file, test_output_file, shallow=False)
