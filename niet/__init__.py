#!/usr/bin/python
import argparse
import json
import sys

from jmespath import search
from jmespath.exceptions import LexerError

import niet.actions as actions
import niet.output as output

import pkg_resources

import yaml


VALID_PRINTERS = {
    "json": {
        "cmd": output.print_json,
        "epilog": "Return object in JSON",
    },
    "yaml": {
        "cmd": output.print_yaml,
        "epilog": "Return object in YAML",
    },
    "eval": {
        "cmd": output.print_eval,
        "epilog": "Return result in a string evaluable by a shell "
        "eval command as an input",
    },
    "newline": {
        "cmd": output.print_newline,
        "epilog": "Return all elements of a list in a new line",
    },
    "ifs": {
        "cmd": output.print_ifs,
        "epilog": "Return all elements of a list separated by IFS env var",
    },
    "squote": {
        "cmd": output.print_squote,
        "epilog": "Add single quotes to result",
    },
    "dquote": {
        "cmd": output.print_dquote,
        "epilog": "Add double quotes to result",
    },
}


def get_epilog():
    epilog = ""
    for item in VALID_PRINTERS:
        epilog += "  {}\t{}\n".format(item, VALID_PRINTERS[item]["epilog"])
    return epilog


# arguments parsing
def argparser():
    epilog = '''output formats:\n{}'''.format(get_epilog())

    parser = argparse.ArgumentParser(
        description='Read data from YAML or JSON file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog)
    parser.add_argument('object', type=str,
                        help="Path to object separated by dot (.). \
                        Use '.' to get whole file. \
                        eg: a.b.c")
    parser.add_argument('file', nargs='?', type=argparse.FileType(),
                        help="Optional JSON or YAML filename. \
                        If not provided niet read from stdin")
    parser.add_argument('-f', '--format', type=str,
                        choices=[key for key in VALID_PRINTERS],
                        help="output format")
    parser.add_argument('-i', '--in-place', action='store_true',
                        help="Perform modification in place. Will so alter \
                        read file")
    parser.add_argument('-o', '--output', type=str, metavar="OUTPUT_FILE",
                        help="Print output in a file instead of stdout \
                        (surcharged by in-place parameter if set)")
    parser.add_argument('-d', '--del', dest='delete', action='append',
                        type=str, metavar=".path.to.object",
                        help="Delete the object)")
    parser.add_argument('-s', '--silent', action='store_true',
                        help="silent mode, doesn't display message when \
                        element was not found")
    parser.add_argument('-v', '--version', action='store_true',
                        help="print the Niet version number and \
                        exit (also --version)")
    return parser.parse_args()


# Parsing to extract wanted object
def data_parser(dataset):
    result = None
    try:
        result = json.loads(dataset)
        in_format = "json"
    except ValueError:
        try:
            result = yaml.safe_load(dataset)
            in_format = "yaml"
        except yaml.constructor.ConstructorError as err:
            print(str(err))
        except yaml.parser.ParserError as err:
            print(str(err))
    if not isinstance(result, (list, dict)):
        print("Invalid file. Only support valid json and yaml input")
        sys.exit(1)
    return result, in_format


# Load file
def get(data, keywords, silent=False):
    if keywords == ".":
        return data
    if keywords.startswith("."):
        keywords = keywords[1:]
    cursor = None
    try:
        try:
            cursor = search(keywords, data)
        except LexerError:
            cursor = search('"{keywords}"'.format(keywords=keywords), data)
        if not cursor:
            raise KeyError()
        return cursor
    except (KeyError, AttributeError):
        if not silent:
            print("Element not found: {research}".format(research=keywords))
        sys.exit(1)


def print_result(res, out_format, in_format, search, out_file):
    if out_format is None:
        if (isinstance(res, (list, str, int, float)) or in_format is None):
            out_format = "newline"
        else:
            out_format = in_format
    try:
        if out_format == "eval":
            output = VALID_PRINTERS[out_format]["cmd"](res, search)
        else:
            # we need to pass the search to init the eval var name
            output = VALID_PRINTERS[out_format]["cmd"](res)
    except KeyError:
        print("Error : Invalid choice")
    else:
        if out_file:
            with open(out_file, "w+") as f:
                f.write(output)
        else:
            print(output)


def get_data(infile):
    with infile:
        return infile.read()


def version():
    installed = pkg_resources.get_distribution('niet').version
    print("niet version {}".format(installed))


# Main
def main():
    if '-v' in sys.argv or '--version' in sys.argv:
        version()
        sys.exit(0)
    args = argparser()
    infile = args.file or sys.stdin
    infilename = args.file.name if args.file else ""
    search = args.object
    dataset = get_data(infile)
    infile.close()
    to_delete = args.delete
    out_format = args.format
    out_file = args.output
    silent = args.silent
    data, in_format = data_parser(dataset)
    result = get(data, search, silent)

    if args.in_place and infilename:
        out_file = infilename

    if to_delete:
        result = actions.delete(result, to_delete)

    print_result(result, out_format, in_format, search, out_file)
