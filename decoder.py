#!/usr/bin/env python

import json

import click
from tabulate import tabulate

SYMBOL_KEY = {
    "wire": "fought",
    "broom": "the children",
    "face": "toys",
    "slashes": "the planes",
    "hourglass": "time",
    "eye": "the power",
    "caret": "gave",
    "caret-with-curve": "give",
    "u": "created",
    "inverted-U": "destroyed",
    "square-with-internal-dots": "trapped",
    "scepter": "life",
    "square-with-external-dots": "freedom",
    "square-with-external-dots-and-curve": "free",
    "star": "everything",
    "arrow": "before",
    "down-arrow": "names",
    "carets": "will give"
}


class ArgumentError(Exception):
    pass


def load_coded_message():
    with open("message.json") as infile:
        content = json.load(infile)
    return content


def apply_symbol_key(coded_message):
    decoded = coded_message.copy()
    for line in decoded:
        for phrase in line:
            for symbol_idx, _ in enumerate(phrase):
                symbol = phrase[symbol_idx]
                if symbol in SYMBOL_KEY:
                    phrase[symbol_idx] = SYMBOL_KEY[symbol].upper()
    return decoded


def format_for_print(line):
    return " ~ ".join([" ".join(p) for p in line])


def print_message(message, display_fmt):
    if display_fmt == "lines":
        for line in message:
            print(format_for_print(line))
            print("")
    elif display_fmt == "phrases":
        for line in message:
            for phrase in line:
                print(" ".join(phrase))
            print("")
    else:
        raise ArgumentError("unknown display type {}".format(display_fmt))


@click.command(name="decode", help="iterate")
@click.option("-d", "--display", "display_fmt", default="lines")
def decode(display_fmt):
    coded_message = load_coded_message()
    decoded = apply_symbol_key(coded_message)
    print_message(decoded, display_fmt)


@click.command(name="freq", help="frequency analysis")
def freq():
    coded_message = load_coded_message()
    symbols = {}
    for line in coded_message:
        for phrase in line:
            for symbol in phrase:
                if symbol in SYMBOL_KEY:
                    continue
                if symbol == "?":
                    continue
                if symbol in symbols:
                    symbols[symbol] = symbols[symbol] + 1
                else:
                    symbols[symbol] = 1
    sorted_symbols = sorted(symbols.items(), key=lambda item: item[1], reverse=True)
    print(tabulate(sorted_symbols))


@click.group()
def main() -> None:
    pass


for func in [decode, freq]:
    main.add_command(func)

if __name__ == "__main__":
    main()
