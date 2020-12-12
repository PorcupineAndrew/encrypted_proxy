#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import click
import sys

def methods(): # NOTE
    return {
        "encode": dummy_encode,
        "decode": dummy_decode,
    }

def dummy_encode(input_string, pkey, skey):
    return input_string[::-1]

def dummy_decode(input_string, pkey, skey):
    return input_string[::-1]


@click.command()
@click.option("--task", "-t", type=click.Choice(["encode", "decode"]), required=True, help="encode or decode")
@click.option("--input-string", "-i", type=str, required=True, help="input string")
@click.option("--pkey", "-p", type=int, required=True, help="public key")
@click.option("--skey", "-s", type=int, required=True, help="secret key")
def main(task, input_string, pkey, skey):
    output_string = methods()[task](input_string, pkey, skey)
    sys.stdout.write(output_string)

if __name__ == "__main__":
    main()
