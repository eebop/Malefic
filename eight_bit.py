from operator import gt, ge, eq, le, lt
import traceback

class eight_bit_signed_integer:
    def __init__(self, input, IsBin=True):
        if IsBin:
            # input is a binary
            multaplier = 1
            if len(input) > 8:
                raise Exception(f'cannot create a {len(input)} value; too high')
            if len(input) == 8 and input[0] == '1':
                multaplier = -1
            self.value = int(input[-7:], 2) * multaplier
        else:
            self.value = input

    def __xor__(self, other):
        if hasattr(other, "value"):
            return self.__class__(self.value ^ other.value, False)
        else:
            return self.__class__(self.value ^ other, False)

    def __add__(self, other):
        if hasattr(other, "value"):
            return self.__class__(self.value + other.value, False)
        else:
            return self.__class__(self.value + other, False)

    def __sub__(self, other):
        if hasattr(other, "value"):
            return self.__class__(self.value - other.value, False)
        else:
            return self.__class__(self.value - other, False)
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return 'eight_bit_signed_integer(' + str(self) + ')' + ('' if self.value.__class__ == int else 'ERR')
    def __and__(self, other):
        print(self.value, other)
        if hasattr(other, "value"):
            return self.__class__(self.value & other.value, False)
        return self.__class__(self.value & other, False)
    def __mul__(self, other):
        return self.value * other
    def __int__(self):
        #print('in __int__')
        #print(repr(self.value))
        return self.value


    def __index__(self):
        return int(self)

    def __abs__(self):
        return abs(self.value)

    def __eq__(self, other):
        if other.__class__ == int:
            return self.value == other
        else:
            return self.value == other.value


    def __gt__(self, other):
        if other.__class__ == int:
            return self.value > other
        else:
            return self.value > other.value

    def __ge__(self, other):
        return gt(self, other) and not eq(self, other)

    def __lt__(self, other):
        return not ge(self, other)

    def __le__(self, other):
        return not gt(self, other)
