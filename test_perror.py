from perror import ErrVal, ezip
import numpy as np

from random import random

def manual_tests():
    #just some calculations to compare to ones i did manually.

    values = list(range(10))
    errors = [1 for _ in values]

    valerrs = np.array(ezip(values, errors))

    avg = np.sum(valerrs / len(valerrs))
    print(avg) # seems plausible


    f = ErrVal(32.76874, 0.39244)
    b = ErrVal(0.01, 5e-5)
    h = ErrVal(0.00145, 5e-5)
    l = ErrVal(0.4, 0.0005)

    e = (12 * f * (l**2)) / (b * (h**3) * (np.pi**2))
    print(e)


def correct(a, b):
    epsilon = 1e-6
    if abs(a - b) > epsilon:
        return False
    return True


def auto_tests():
    testnum = 1_000
    lim = 1000
    for _ in range(testnum):
        a = random() * lim
        b = random() * lim

        fp_res = a + b
        ev_res = ErrVal(a, 0) + ErrVal(b, 0)
        if not correct(fp_res, ev_res):
            print("add failed with", a, b)

        fp_res = a - b
        ev_res = ErrVal(a, 0) - ErrVal(b, 0)
        if not correct(fp_res, ev_res):
            print("sub failed with", a, b)

        fp_res = a * b
        ev_res = ErrVal(a, 0) * ErrVal(b, 0)
        if not correct(fp_res, ev_res):
            print("mul failed with", a, b)

        fp_res = a / b
        ev_res = ErrVal(a, 0) / ErrVal(b, 0)
        if not correct(fp_res, ev_res):
            print("div failed with", a, b)



        fp_res = a + b
        ev_res = ErrVal(a, 0) + b
        if not correct(fp_res, ev_res):
            print("add failed with mixed", a, b)

        fp_res = a - b
        ev_res = ErrVal(a, 0) - b
        if not correct(fp_res, ev_res):
            print("sub failed with mixed", a, b)

        fp_res = a * b
        ev_res = ErrVal(a, 0) * b
        if not correct(fp_res, ev_res):
            print("mul failed with mixed", a, b)

        fp_res = a / b
        ev_res = ErrVal(a, 0) / b
        if not correct(fp_res, ev_res):
            print("div failed with mixed", a, b)



        fp_res = a + b
        ev_res = a + ErrVal(b, 0)
        if not correct(fp_res, ev_res):
            print("add failed with left mixed", a, b)

        fp_res = a - b
        ev_res = a - ErrVal(b, 0)
        if not correct(fp_res, ev_res):
            print("sub failed with left mixed", a, b)

        fp_res = a * b
        ev_res = a * ErrVal(b, 0)
        if not correct(fp_res, ev_res):
            print("mul failed with left mixed", a, b)

        fp_res = a / b
        ev_res = a / ErrVal(b, 0)
        if not correct(fp_res, ev_res):
            print("div failed with left mixed", a, b)


def main():
    auto_tests()
    manual_tests()

if __name__ == '__main__':
    main()