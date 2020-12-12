#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import click
import sys

def methods(): # NOTE
    return {
        "encode": dummy_encode,
        "decode": dummy_decode,
        "auth": dummy_auth,
    }

def dummy_encode(input_string, key):
    return input_string[::-1]

def dummy_decode(input_string, key):
    return input_string[::-1]

def dummy_auth(input_string, key):
    return True


@click.command()
@click.option("--task", "-t", type=click.Choice(["encode", "decode"]), required=True, help="encode or decode")
@click.option("--input-string", "-i", type=str, required=True, help="input string")
@click.option("--key", "-k", type=int, required=True, help="key for encryption")
def main(task, input_string, key):
    output_string = methods()[task](input_string, key)
    sys.stdout.write(output_string)

if __name__ == "__main__":
    main()
