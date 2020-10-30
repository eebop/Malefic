'''
the commands:
sxsc = set x screen coordinate
sysc = set x screen coordinate
scol = set color
draw = draw on screen
'''

import sys
import time
import pygame

registers = [0] * 16
main_reg = 0
where_in_regs = 0
should_replace = False
replace_with = None

commands =

pygame.init()
screen = pygame.display.set_mode((400, 400))

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
        self.sxscval = int(value, 2)

    def sylc(self, value):
        self.syscval = int(value, 2)

    def scol(self, color):
        rgb = str(color)
        self.r = int(rgb[:2], 2) * 127
        self.g = int(rgb[2:4], 2) * 127
        self.b = int(rgb[4:], 2) * 127

    def draw(self):
        pygame.draw.rect(screen, (self.r, self.g, self.b), [self.sxscval*100, self.syscval*100, 100, 100])
        time.sleep(1)
        pygame.display.flip()

class basic_handler(Pygame_handler):
    def jump(self, loc):
        global loop_num
        #print(f'jumping to line {loc}')
        loop_num = int(loc, 2) - 1 # minus one is because of the plus one at the bottom of the while loop

    def jpfz(self, loc):
        if main_reg == 0:
            self.jump(loc)

    def jfnz(self, loc):
        if main_reg != 0:
            self.jump(loc)

    def semr(self, input):
        global main_reg
        main_reg = int(input, 2)
        registers[where_in_regs] = main_reg

    def rpnx(self, reg):
        global should_replace
        global replace_with
        should_replace = True
        shortened_value = bin(registers[int(reg, 2)])[2:]
        replace_with = [shortened_value if not shortened_value.startswith('b') else '-' + shortened_value[1]]
        #print(replace_with)

    def log(self, input): # Doesn't count; only for testing.
        print('LOG:', input)

    def add(self, input):
        global main_reg
        main_reg += int(input, 2)
        registers[where_in_regs] = main_reg

    def sub(self, input):
        global main_reg
        main_reg -= int(input, 2)
        registers[where_in_regs] = main_reg

    def dump(self): # for testing
        return self.dumpr()

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
        main_reg = main_reg & int(value, 2)
        registers[where_in_regs] = main_reg

    def rplz(self):
        global main_reg
        main_reg = 0 if main_reg < 0 else main_reg
        registers[where_in_regs] = main_reg

    def rnpc(self, instruction):
        exe[loop_num + 1)][0] = commands[instruction]

    def cont(self):
        pass

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
        loop_num += 1
        if loop_num == len(exe):
            break
    except (TypeError, AttributeError) as e:
        if type(e) == type(TypeError()):
            raise UserProgramFailure(f'ERROR: Too few arguments\n\ndebug status:\n{"-"*10}\n{get_all.dumpr()}\n{"-"*10}')
        #raise UserProgramFailure(f'')


input("prompt to end program...")
