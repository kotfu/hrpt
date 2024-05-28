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

import hrpt

EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_USAGE = 2


def _build_parser():
    """build an arg parser with all the proper parameters"""
    desc = "Ham Radio Programming Toolkit"
    epilog = """"""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc,
        epilog=textwrap.dedent(epilog),
    )

    input_file_help = "file to read input from"
    parser.add_argument("-i", "--input-file", help=input_file_help)

    output_file_help = "file to write output to"
    parser.add_argument("-o", "--output-file", help=output_file_help)

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
    argparser = _build_parser()
    args = argparser.parse_args(argv)

    parser = hrpt.parsers.CHIRPParser()
    # TODO maybe the open should be encapsulated in the parser because
    # the CSV module needs newline=''
    if args.input_file:
        with open(args.input_file, encoding="utf8", newline="") as fileobj:
            memories = parser.parse(fileobj)
    else:
        memories = parser.parse(sys.stdin)

    # TODO maybe the open should be encapsulated in the renderer?
    renderer = hrpt.renderers.ADMS16Renderer()
    if args.output_file:
        with open(args.output_file, mode="w", encoding="utf8", newline="\n") as fileobj:
            renderer.render(memories, fileobj)
    else:
        renderer.render(memories, sys.stdout)

    return EXIT_SUCCESS


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
