import random
import math

def quickpowmod(a, k, n):
    a = a % n
    ans = 1
    while k != 0:
        if k & 1:
            ans = (ans * a) % n
        a = (a * a) % n
        k >>= 1
    return ans

def exeuclid(a, b, lst):
    #print(a, b, lst)
    if b == 0:
        lst[0] = 1
        lst[1] = 0
        lst[2] = a
    else:
        exeuclid(b, a % b, lst)
        #print(a, b, lst)
        t = lst[0]
        lst[0] = lst[1]
        lst[1] = t - (a // b) * lst[1]

def modinverse(n, a):
    if a > n:
        a = a % n
    lst = [0, 0, 0]
    exeuclid(n, a, lst)
    #print(n, a, lst, n * lst[0] + a * lst[1])
    if lst[2] == 1:
        return lst[1] % n
    else:
        return -1

def millerwitness(a, n):
    if n == 1:
        return False
    if n == 2:
        return True
    k = n - 1
    q = int(math.floor(math.log(k, 2)))
    while q > 0:
        if k % (2 ** q) == 0:
            break
        q -= 1
    if quickpowmod(a, n - 1, n) != 1:
        return False
    m = int(k / (2 ** q))
    b1 = quickpowmod(a, m, n)
    if b1 == 1:
        return True
    for i in range(0, q):
        if b1 == n - 1:
            return True
        b1 = (b1 ** 2) % n
    return False

def primetest(p, k):
    lst = []
    while k > 0:
        a = random.randint(1, p - 1)
        lst.append(a)
        if not millerwitness(a, p):
            #print(lst)
            return False
        k -= 1
    #print(lst)
    return True

def produceprime(n):
    count = 0
    ans = []
    for i in range(2, n + 1):
        if primetest(i, 8):
            #print(i)
            ans.append(i)
            count += 1
    # print(count)
    return ans

