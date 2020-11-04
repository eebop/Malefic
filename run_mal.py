import sys
import time
import pygame
import data
from gen_new_updated_file import gen_file, format_prog
from eight_bit import eight_bit_signed_integer

registers = [eight_bit_signed_integer('0')] * 128
main_reg = 0
where_in_regs = 0
should_replace = False
replace_with = None


commands_dict = data.data

pygame.init()
screen = pygame.display.set_mode((512, 512))

with open(sys.argv[1], 'r') as f:
    txt = f.read()

exe = list(map(str.split, txt.splitlines()))

class UserProgramFailure(Exception):
    pass

class Pygame_handler:
    '''WARNING: only make one instance'''
    def __init__(self):

        self.sxscval = -1
        self.syscval = -1

    def sxlc(self, value):
        self.sxscval = eight_bit_signed_integer(value)

    def sylc(self, value):
        self.syscval = eight_bit_signed_integer(value)

    def scol(self, color):
        rgb = str(color)
        self.r = eight_bit_signed_integer(rgb[:2]) * 127
        self.g = eight_bit_signed_integer(rgb[2:4]) * 127
        self.b = eight_bit_signed_integer(rgb[4:]) * 127

    def draw(self):
        pygame.gfxdraw.pixel(screen, (self.r, self.g, self.b), [self.sxscval*2, self.syscval*2, 2, 2])
        time.sleep(1)
        pygame.display.flip()

class basic_handler(Pygame_handler):
    def jump(self, loc):
        global loop_num
        #print(f'jumping to line {loc}')
        loop_num = eight_bit_signed_integer(loc) - 1 # minus one is because of the plus one at the bottom of the while loop

    def jpfz(self, loc):
        if main_reg == 0:
            self.jump(loc)

    def jfnz(self, loc):
        if main_reg != 0:
            self.jump(loc)

    def semr(self, input):
        global main_reg
        main_reg = eight_bit_signed_integer(input)
        registers[where_in_regs] = main_reg

    def rpnx(self, reg):
        global should_replace
        global replace_with
        should_replace = True
        #print(repr(reg))
        #print(int(eight_bit_signed_integer(reg)))
        #print(registers[int(eight_bit_signed_integer(reg))])
        #print(bin(registers[int(eight_bit_signed_integer(reg))])[2:])
        shortened_value = bin(registers[int(eight_bit_signed_integer(reg))])[2:]
        replace_with = [shortened_value if not shortened_value.startswith('b') else '-' + shortened_value[1:]]
        #print(replace_with)

    def log(self, input): # Doesn't count; only for testing.
        print('LOG:', input)

    def add(self, input):
        global main_reg
        main_reg += eight_bit_signed_integer(input)
        registers[where_in_regs] = main_reg

    def sub(self, input):
        global main_reg
        main_reg -= eight_bit_signed_integer(input)
        registers[where_in_regs] = main_reg

    def dump(self): # for testing
        print(self.dumpr())

    def dumpr(self): # DO NOT USE IN SIM
        return f'''On line {loop_num}. The program is {len(exe)} lines long.
The registers contain {registers},\nof which register {where_in_regs} is the main one.
it contains {main_reg}.'''

    def swir(self, reg):
        reg = int(reg, 2)
        global main_reg
        global where_in_regs
        registers[where_in_regs] = main_reg
        main_reg = registers[reg]
        where_in_regs = reg

    def kill(self): # Doesn't count; only for testing.
        time.sleep(10)
        sys.exit()

    def abs(self): # can use boolean and instead in other implamentations
        global main_reg
        main_reg = abs(main_reg)
        registers[where_in_regs] = main_reg

    def band(self, value):
        global main_reg
        main_reg = main_reg & eight_bit_signed_integer(value) #main_reg is a eight_bit_signed_integer
        registers[where_in_regs] = main_reg

    def rplz(self):
        global main_reg
        main_reg = 0 if main_reg < 0 else main_reg
        registers[where_in_regs] = main_reg

    def rein(self, instruction):
        exe[main_reg][0] = commands_dict[instruction.zfill(4)]

    def cont(self):
        pass

    def xor(self, value):
        global main_reg
        main_reg = main_reg ^ eight_bit_signed_integer(value)
        registers[where_in_regs] = main_reg

get_all = basic_handler()

loop_num = 0



while True:
    try:
        if exe[loop_num]:
            program, *value = exe[loop_num][:2]
            if not program.startswith('#'):
                if should_replace:
                    value = replace_with
                    should_replace = False
                if value and value[0].startswith('#'): # This shorts out if value is empty
                    value = []
                getattr(get_all, program)(*value)
        #print('here')
        loop_num += 1
        if loop_num == len(exe):
            break
    except Exception:
        raise UserProgramFailure(f'ERROR:\n\ndebug status:\n{"-"*10}\n{get_all.dumpr()}\n{"-"*10}')
    #get_all.dump()


input("prompt to end program...")

gen_file(txt, format_prog(exe), sys.argv[1])
