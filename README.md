# Malefic
A turing complete simulator
M. A. L. E. F. I. C. (Miniature Assembly LanguagE For Internal Computing)

MALEFIC utilizes a unusual type of machine language, and therefore a unusual assembly language

All memory except from "special" memory is basically held in registers. There is a main register which is
the default for the output of operations, and is also used as the input. The main register can be changed (see swir).
If a program calls for a word of special memory, it is pulled off the top of the stack and the next one is selected
(however, it can be replaced with a value from a register. See rpnx).
All words are equivalent to one signed byte, and all programs are half a word long.

The assembly language is in the format
<command> <optional special memory value (in binary)> <optional comment>
or
\# <optional comment>
or
<newline>


note that everything  in binary

the explanation is of the type

  name (lengthened name)(value, if necessary to load from special memory) <location>

    cont (continue)() 0b0000
      do nothing

screen commands

    scol (set the color)(color) 0b0001
      the color is parsed like this: The lowest two digits are the blue color, the middle two
      are green, and the two higher than that are blue. Note that the +/- sign and the highest digit
      are not used

    sxlc (set x location)(x location) 0b0010
      set the x value of the screen pointer

    sysc (set y location)(y location) 0b0011
      set the x value of the screen pointer

    draw (draw)() 0b0100
      draw the  color on the screen at the intersection of the

other commands:

    jump (jump)(line) 0b0101
      jump to (absolute) line <line>

    jpfz (jump if zero)(line) 0b0110
      jump to line <line> if the main register contains zero

    jfnz (jump if not zero)(line) 0b0111
      jump to line <line> if the main register does not contain zero

    semr (set the main register)(value) 0b1000
      set the main register to <value>

    rpnx (replace next)(reg) 0b1001
      instead of the next instruction from special memory,
      load it from the word in register reg

    add (add)(value) 0b1010
      add value to main register, and place it in the main register

    sub (sub)(value) 0b1011
      subtract value from main register, and place it in the main register

    swir (switch register) (reg) 0b1100
      set the main register to register <reg>

    band (boolean and) (value) 0b1101
      boolean and value and main register together, putting the output into main register

    rplz (replace if zero)() 0b1110
      if main register contains a value that is less than zero, replace it with zero

    rnxi (replace next instruction)(instruction) 0b1111 NOT IMPLEMENTED
      replace the next instruction with instruction <instruction>
