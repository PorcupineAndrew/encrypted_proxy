import functions
import random

def producekey(k):
    primelst = functions.produceprime(1000)
    f = 2
    p = []
    while f > 0 :
        r = random.randint(2 ** k, 2 ** (k + 5))
        r = 2 * r + 1
        l = True
        while l:
            l = False
            for i in primelst:
                if r % i == 0:
                    r += 2
                    l = True
                    break
        if functions.primetest(r, 10):
            f -= 1
            p.append(r)
    n = p[0] * p[1]
    fin = (p[0] - 1) * (p[1] - 1)
    l = True
    e = 0
    d = 0
    while l:
        d = random.randint(int(p[0] / 5), p[0])
        e = functions.modinverse(fin, d)
        if e != -1:
            l = False
    # print(d, e, n)
    # print((d * e) % fin)
    return d, e, n

d, e, n = producekey(60)
