import argparse
import sys

from formats import flightgear, simbrief

import_formats = {"simbrief": simbrief}
export_formats = {"flightgear": flightgear}

argparser = argparse.ArgumentParser()
argparser.add_argument("input",
        help="the name of the file to convert to another format")
argparser.add_argument("-f", "--input-format",
        help="the format of the input file (default is simbrief)",
        default="simbrief", choices=import_formats.keys())
argparser.add_argument("-F", "--output-format",
        help="the format of the output file (default is flightgear)",
        default="flightgear", choices=export_formats.keys())
argparser.add_argument("-o", "--output",
        help="the name of the file to which to write the flight plan")
args = argparser.parse_args()

if args.input == "-":
    # This reads until EOF, or Ctrl + D
    input_contents = sys.stdin.read()
else:
    with open(args.input, "r", encoding="utf8") as f:
        input_contents = f.read()

flightplan = import_formats[args.input_format].import_fp(input_contents)
exported_fp = export_formats[args.output_format].export_fp(flightplan)

if not args.output:
    print(exported_fp)
else:
    with open(args.output, "w") as f:
        f.write(exported_fp)
