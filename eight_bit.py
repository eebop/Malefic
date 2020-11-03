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

    def __add__(self, other):
        return self.__class__(self.value + other.value, False)

    def __sub__(self, other):
        return self.__class__(self.value - other.value, False)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

    def __and__(self, other):
        return self.__class__(self.value & other.value)

    def __mul__(self, other):
        return self.value * other

    def __int__(self):
        print('in __int__')
        print(repr(self.value))
        return self.value
