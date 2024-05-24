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
Entry point for 'hrpt' command line program.
"""
import argparse
import sys
import textwrap

EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_USAGE = 2

import hrpt

def _build_parser():
    """build an arg parser with all the proper parameters"""
    desc = "Ham Radio Programming Toolkit"
    epilog = """"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc,
        epilog=textwrap.dedent(epilog),
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=hrpt.VERSION_STRING,
        help="show the version information and exit",
    )
    return parser


def main(argv=None):
    """main function"""
    parser = _build_parser()
    args = parser.parse_args(argv)

    return EXIT_SUCCESS


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
