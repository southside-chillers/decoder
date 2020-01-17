#!/usr/bin/env python

import json

import click

SYMBOL_KEY = {"wire": "fight"}


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


def print_message(message):
    for line in message:
        print(format_for_print(line))
        print("")


@click.command(name="experiment", help="iterate")
def experiment():
    coded_message = load_coded_message()
    decoded = apply_symbol_key(coded_message)
    print_message(decoded)


@click.group()
def main() -> None:
    pass


for func in [experiment]:
    main.add_command(func)

if __name__ == "__main__":
    main()
