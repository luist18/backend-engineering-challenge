import argparse
import os
import sys

import unbabel_cli.algorithm as algorithm
from unbabel_cli.util.file import read_input_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unbabel CLI")
    parser.add_argument("--input_file", help="Input file path", required=True, type=str)
    parser.add_argument(
        "--window_size", help="Window size. Must be zero or a positive integer", required=True, type=int
    )
    parser.add_argument(
        "--algorithm",
        help='Moving average algorithm. Values: "hash_map" or "queue". Default: "hash_map"',
        required=False,
        type=str,
        default="hash_map",
    )
    args = parser.parse_args()

    # Check if input file exists
    if not os.path.isfile(args.input_file):
        sys.exit("The input file does not exist. Exiting...")

    # Check if window size is a positive integer or zero
    if args.window_size < 0:
        sys.exit("The window size must be a positive integer. Exiting...")

    # Check algorithm value
    if args.algorithm not in algorithm.algorithms:
        sys.exit("The algorithm is not valid. Exiting...")

    # Check if input file has valid data
    try:
        input = read_input_file(args.input_file)
    except Exception as e:
        sys.exit("The input file has invalid data. Exiting...")

    # Call the algorithm
    output = algorithm.algorithms[args.algorithm]().moving_average(input, args.window_size)

    # sys output the output in separate lines
    output_text = "\n".join([str(output) for output in output])

    sys.stdout.write(output_text)
