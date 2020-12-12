#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import click
import sys
import math
import functions

def methods(): # NOTE
    return {
        "encode": dummy_encode,
        "decode": dummy_decode,
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
        #print(st, ed, mm)
        o = ed - st + 1
        p = 8 * o - (i * k) % 8
        r = (2 ** p) - 1
        mm &= r
        q = 8 - 1 - ((i + 1) * k - 1) % 8
        mm >>= q
        #print(mm)
        w = functions.quickpowmod(mm, d, n)
        #print(w)
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
        #print(mm)
        wl = functions.quickpowmod(mm, d, n)
        #print(wl)
        for j in range(k, -1, -1):
            if wl & (1 << j):
                s += '1'
            else:
                s += '0'
    #print(s)
    while len(s) % 8 != 0:
        s += '0'
    ls = len(s)
    ans = ''
    for i in range(0, ls, 8):
        ss = s[i:i+8]
        #print(s[i:i+8], int(ss, 2))
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
        #print(st, ed, mm)
        o = ed - st + 1
        p = 8 * o - (i * k) % 8
        r = (2 ** p) - 1
        mm &= r
        q = 8 - 1 - ((i + 1) * k - 1) % 8
        mm >>= q
        #print(mm)
        w = functions.quickpowmod(mm, d, n)
        #print(w)
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
        #print(mm)
        wl = functions.quickpowmod(mm, d, n)
        #print(wl)
        for j in range(k - 2, -1, -1):
            if wl & (1 << j):
                s += '1'
            else:
                s += '0'
    #print(s)
    while len(s) % 8 != 0:
        s += '0'
    ls = len(s)
    ans = ''
    for i in range(0, ls, 8):
        ss = s[i:i+8]
        #print(s[i:i+8], int(ss, 2))
        ans += (chr(int(ss, 2)))
    while ans[-1] == '\0':
        ans = ans[:-2]
    return bytes(ans, encoding='latin1')

def dummy_encode(input_string, pkey, skey):
    strb = bytes(input_string, encoding='latin1')
    strcb = encrypt(strb, skey[0], skey[1])
    print(strcb)
    strret = encrypt(strcb+b'hello bro!', pkey[0], pkey[1])
    return strret

def dummy_decode(input_string, pkey, skey):
    strb = bytes(input_string, encoding='latin1')
    strcb = decrypt(strb, skey[0], skey[1])
    print(strcb)
    if  strcb[-10:] != b'hello bro!':
        exit(0)
    strret = decrypt(strcb[:-10], pkey[0], pkey[1])
    return strret


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
