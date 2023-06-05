from dataclasses import dataclass
from math import sqrt, log10, log
from numba import njit

def sq(a):
    return a ** 2


def const_err(e):
    return lambda v: make_errval(v, e)


def make_errval(v, e):
    return ErrVal(v, e)


def ezip(values, errors):
    return [ErrVal(values[i], errors[i]) for i in range(len(values))]


num_type = [float, int]


@dataclass
class ErrVal:
    value : float
    error : float

    def __init__(self, v, e):
        self.value = v
        self.error = abs(e)

    def __gt__(self, other):
        if type(other) in num_type:
            other = ErrVal(other, 0)

        return self.value > other.value


    def __add__(self, other):
        if type(other) in num_type:
            other = ErrVal(other, 0)

        v = self.value + other.value
        
        # add errors using gaussion error propagation
        e = sqrt(sq(self.error) + sq(other.error))

        return ErrVal(v, e)


    def __sub__(self, other):
        return self + (-1 * other)


    def __rsub__(self, other):
        return other + (-1 * self)


    def __radd__(self, other):
        return self + other 
        

    def __rmul__(self, other):
        return self * other


    def __rtruediv__(self, other):
        temp = ErrVal(1, 0)
        return other * (temp / self)


    def __mul__(self, other):
        if type(other) in num_type:
            other = ErrVal(other, 0)

        v = self.value * other.value
        e = sqrt(sq(other.value * self.error) + sq(self.value * other.error))

        return ErrVal(v, e)


    def __truediv__(self, other):
        if type(other) in num_type:
            other = ErrVal(other, 0)

        v = self.value / other.value
        e = sqrt(sq(self.error / other.value) + sq(other.error * self.value / sq(other.value)))

        return ErrVal(v, e)


    def __pow__(self, exp):
        if type(exp) in num_type:
            exp = ErrVal(exp, 0)

        v = self.value ** exp.value
        e = sqrt(sq(exp.value * (self.value ** (exp.value - 1)) * self.error) + sq((self.value ** exp.value) * log(self.value) * exp.error))

        return ErrVal(v, e)


    def __rpow__(self, other):
        other = ErrVal(other, 0)
        return other ** self


    def __abs__(self):
        return ErrVal(abs(self.value), self.error)


    def __float__(self):
        return float(self.value)


    def __int__(self):
        return int(self.value)


    def __str__(self):
        err_magn = int(log10(self.error))
        val_magn = int(log10(self.value))

        exponent = - min(err_magn, val_magn)
        significant = 1 + abs(err_magn - exponent)

        fmt = "( "
        fmt += str(round(self.value * (10 ** exponent), significant))
        fmt += " +- "
        fmt += str(round(self.error * (10 ** exponent), significant))
        fmt += " ) * 10^" + str(- exponent)

        return fmt
