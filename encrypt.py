#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import click
import sys
import math
import functions

def methods(): # NOTE
    return {
        "encode": encode,
        "decode": decode,
    }

def encrypt(strb, d, n):
    k = math.floor(math.log(n, 2))
    b = math.floor((len(strb) * 8) / k)
    s = ''
    for i in range(b):
        st = math.floor((i * k) / 8)
        ed = ((i + 1) * k - 1) // 8
        m = []
        for j in strb[st:ed + 1]:
            m.append(j)
        mm = 0
        for j in m:
            mm *= 2 ** 8
            mm += j
        o = ed - st + 1
        p = 8 * o - (i * k) % 8
        r = (2 ** p) - 1
        mm &= r
        q = 8 - 1 - ((i + 1) * k - 1) % 8
        mm >>= q
        w = functions.quickpowmod(mm, d, n)
        for j in range(k, -1, -1):
            if w & (1 << j):
                s += '1'
            else:
                s += '0'
    if (len(strb) * 8) % k != 0:
        stl = math.floor((b * k) / 8)
        m = []
        for j in strb[stl:]:
            m.append(j)
        mm = 0
        for j in m:
            mm *= 2 ** 8
            mm += j
        ol = len(strb) - stl
        pl = 8 * ol - (b * k) % 8
        rl = (2 ** pl) - 1
        mm &= rl
        mm <<= (b + 1) * k - len(strb) * 8
        wl = functions.quickpowmod(mm, d, n)
        for j in range(k, -1, -1):
            if wl & (1 << j):
                s += '1'
            else:
                s += '0'
    while len(s) % 8 != 0:
        s += '0'
    ls = len(s)
    ans = ''
    for i in range(0, ls, 8):
        ss = s[i:i+8]
        ans += (chr(int(ss, 2)))
    return bytes(ans, encoding='latin1')

def decrypt(strb, d, n):
    k = math.floor(math.log(n, 2) + 1)
    b = math.floor((len(strb) * 8) / k)
    s = ''
    for i in range(b):
        st = math.floor((i * k) / 8)
        ed = ((i + 1) * k - 1) // 8
        m = []
        for j in strb[st:ed + 1]:
            m.append(j)
        mm = 0
        for j in m:
            mm *= 2 ** 8
            mm += j
        o = ed - st + 1
        p = 8 * o - (i * k) % 8
        r = (2 ** p) - 1
        mm &= r
        q = 8 - 1 - ((i + 1) * k - 1) % 8
        mm >>= q
        w = functions.quickpowmod(mm, d, n)
        for j in range(k - 2, -1, -1):
            if w & (1 << j):
                s += '1'
            else:
                s += '0'
    if (len(strb) * 8) % k != 0:
        stl = math.floor((b * k) / 8)
        m = []
        for j in strb[stl:]:
            m.append(j)
        mm = 0
        for j in m:
            mm *= 2 ** 8
            mm += j
        ol = len(strb) - stl
        pl = 8 * ol - (b * k) % 8
        rl = (2 ** pl) - 1
        mm &= rl
        mm <<= (b + 1) * k - len(strb) * 8
        wl = functions.quickpowmod(mm, d, n)
        for j in range(k - 2, -1, -1):
            if wl & (1 << j):
                s += '1'
            else:
                s += '0'
    while len(s) % 8 != 0:
        s += '0'
    ls = len(s)
    ans = ''
    for i in range(0, ls, 8):
        ss = s[i:i+8]
        ans += (chr(int(ss, 2)))
    while ans[-1] == '\0':
        ans = ans[:-1]
    return bytes(ans, encoding='latin1')

def encode(input_string, pkey, skey):
    strb = bytes(input_string, encoding='latin1')
    strcb = encrypt(strb, skey[0], skey[1])
    strret = encrypt(strcb+b'hello bro!', pkey[0], pkey[1])
    strret = strret.decode(encoding="latin1")
    return strret

def decode(input_string, pkey, skey):
    strb = bytes(input_string, encoding='latin1')
    strcb = decrypt(strb, skey[0], skey[1])
    if  strcb[-10:] != b'hello bro!':
        sys.stderr.write("exit 2")
        exit(2)
    strret = decrypt(strcb[:-10], pkey[0], pkey[1])
    strret = strret.decode(encoding="latin1")
    return strret


@click.command()
@click.option("--task", "-t", type=click.Choice(["encode", "decode"]), required=True, help="encode or decode")
@click.option("--input-string", "-i", type=str, required=True, help="input string file")
@click.option("--pkey", "-p", type=str, required=True, help="public key")
@click.option("--skey", "-s", type=str, required=True, help="secret key")
def main(task, input_string, pkey, skey):
    if task == "decode":
        input_string = open(input_string, "rb").read().decode()
    pkey = list(map(int, pkey.strip().split(" ")))
    skey = list(map(int, skey.strip().split(" ")))
    output_string = methods()[task](input_string, pkey, skey)
    sys.stdout.write(output_string)

if __name__ == "__main__":
    main()
