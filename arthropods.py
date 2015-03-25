#!/usr/bin/python
import getopt, sys
from fpgen import *

STYLE_THICKENED, STYLE_DENT, STYLE_BOXED, \
    STYLE_WSL_ARROW, STYLE_WSL_DENT, STYLE_PSL = xrange(6)
SHAPE_STRAIGHT, SHAPE_ZIGZAG, SHAPE_USHAPED = xrange(3)

pin_thickness = 1.5 # mm
pin_clearance = 1. # mm
pin_mask = 1.6 # mm
pin_drill = 1. # mm

pad_thickness = 1.492 # mm
pad_clearance = 1. # mm
pad_mask = 1.59 # mm

def invalid_arguments(message):
    sys.stderr.write("%s: %s\n" % (sys.argv[0], message))
    sys.stderr.write("Try `%s --help' for more information.\n" % sys.argv[0])
    sys.exit(1)

def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:], 's:ZUd:', ['style=', 'straight', 'zigzag', 'u-shaped',
                                     'row-distance=', 'help', 'version'])
    except getopt.GetoptError as e:
        invalid_arguments(e.msg)

    style = STYLE_THICKENED
    shape = SHAPE_STRAIGHT
    row_distance = 100

    for option, value in options:
        if option in ['-s', '--style']:
            try:
                style = { 'thickened': STYLE_THICKENED,
                          'dent': STYLE_DENT,
                          'boxed': STYLE_BOXED,
                          'wsl-arrow': STYLE_WSL_ARROW,
                          'wsl-dent': STYLE_WSL_DENT,
                          'psl': STYLE_PSL
                }[value]
            except KeyError:
                invalid_arguments("`%s' is not a valid silk style" % value)
        elif option == '--straight':
            shape = SHAPE_STRAIGHT
        elif option in ['-Z', '--zigzag']:
            shape = SHAPE_ZIGZAG
        elif option in ['-U', '--u-shaped']:
            shape = SHAPE_USHAPED
        elif option in ['-d', '--row-distance']:
            try:
                row_distance = int(value)
            except ValueError:
                invalid_arguments("`%s' is not an integer" % value)
        elif option == '--help':
            sys.stdout.write("Usage: %s NAME PIN_COUNT\n" % sys.argv[0])
            sys.stdout.write("\n")
            sys.stdout.write(
"      -s, --style=thickened|dent|boxed|wsl-arrow|wsl-dent|psl\n"
"                        use this style to indicate pin 1 on the silk layer\n")
            sys.stdout.write("\n")
            sys.stdout.write(
"      --straight        one straight row of pins\n"
"      -Z, --zigzag      two rows of pins, numbered in zig-zag\n"
"      -U, --u-shaped    two rows of pins, numbered in an U shape\n"
"      -d, --row-distance  distance between the rows, as a number in mils\n")
            sys.stdout.write("\n")
            sys.stdout.write(
"      --help            give this help\n"
"      --version         display version number\n")
            sys.exit(0)
        elif option == '--version':
            xorn.command.core_version()
        else:
            raise AssertionError

    try:
        name, pin_count_str = args
    except ValueError:
        sys.stdout.write("Usage: %s NAME PIN_COUNT\n" % sys.argv[0])
        sys.stderr.write("Try `%s --help' for more information.\n"
                         % sys.argv[0])
        sys.exit(1)

    try:
        pin_count = int(pin_count_str)
    except ValueError:
        invalid_arguments("`%s' is not an integer" % pin_count_str)

    if shape != SHAPE_STRAIGHT and pin_count % 2 != 0:
        invalid_arguments("Pin count for zigzag/u-shaped shape must be even")

    if shape == SHAPE_STRAIGHT:
        rows = 1
        row_distance = 0
    elif shape == SHAPE_ZIGZAG:
        rows = 2
    elif shape == SHAPE_USHAPED:
        rows = 2
    else:
        raise ValueError

    eff_pin_count = pin_count // rows

    # Calculate dimensions

    width = float(row_distance)
    height = (eff_pin_count - 1) * 100

    if style in [STYLE_WSL_ARROW, STYLE_WSL_DENT]:
        x_offset = 125.
        y_offset = 200.
    else:
        x_offset = 50.
        y_offset = 50.

    x0 = -x_offset; x1 = width + x_offset
    y0 = -y_offset; y1 = height + y_offset

    if style == STYLE_DENT:
        text_x, text_y, text_dir, text_scale = \
          '%dmil' % (width / 2 + 30.), '25mil', 3, 100
    elif style == STYLE_PSL:
        text_x, text_y, text_dir, text_scale = \
          '-68.11mil', '-506.69mil', 0, 100
    elif shape == SHAPE_STRAIGHT:
        text_x, text_y, text_dir, text_scale = \
          '%dmil' % (x1 + 70.), '%dmil' % (y0 + 5.), 3, 100
    else:
        text_x, text_y, text_dir, text_scale = \
          '%dmil' % x0, '%dmil' % (y0 - 70.), 0, 100

    start(None, name, name, name, 0., 0.,
          text_x, text_y, text_dir, text_scale, None)

    for i in xrange(0, eff_pin_count):
        y = '%dmil' % (i * 100)
        if i == 0:
            maybe_square = ['square']
        else:
            maybe_square = []

        if shape == SHAPE_ZIGZAG:
            i0, i1 = i * 2 + 1, i * 2 + 2
        if shape == SHAPE_USHAPED:
            i0, i1 = i + 1, pin_count - i

        if shape == SHAPE_STRAIGHT:
            pin(0., y, pin_thickness, pin_clearance, pin_mask, pin_drill,
                i + 1, flags = maybe_square)
            pad('-25mil', y, '25mil', y,
                pad_thickness, pad_clearance, pad_mask,
                i + 1, flags = ['onsolder'] + maybe_square)
        elif row_distance < 150:
            pin('0mil', y,
                pin_thickness, pin_clearance, pin_mask, pin_drill,
                i0, flags = maybe_square)
            pin('%dmil' % width, y,
                pin_thickness, pin_clearance, pin_mask, pin_drill, i1)
            pad('-50mil', y, '0mil', y,
                pad_thickness, pad_clearance, pad_mask,
                i0, flags = ['onsolder'] + maybe_square)
            pad('%dmil' % width, y, '%dmil' % (width + 50), y,
                pad_thickness, pad_clearance, pad_mask,
                i1, flags = ['onsolder', 'edge2'])
        else:
            pin('0mil', y,
                pin_thickness, pin_clearance, pin_mask, pin_drill,
                i0, flags = maybe_square)
            pad('-25mil', y, '25mil', y,
                pad_thickness, pad_clearance, pad_mask,
                i0, flags = ['onsolder'] + maybe_square)
            pin('%dmil' % width, y,
                pin_thickness, pin_clearance, pin_mask, pin_drill, i1)
            pad('%dmil' % (width - 25.), y, '%dmil' % (width + 25.), y,
                pad_thickness, pad_clearance, pad_mask,
                i1, flags = ['onsolder', 'edge2'])

    # Paint outline

    if style == STYLE_THICKENED:
        # thick line
        line('%dmil' % x0, '%dmil' % y0,
             '%dmil' % x1, '%dmil' % y0, '10mil')
        line('%dmil' % x0, '%dmil' % (y0 + 5),
             '%dmil' % x1, '%dmil' % (y0 + 5), '10mil')
        line('%dmil' % x0, '%dmil' % (y0 + 10),
             '%dmil' % x1, '%dmil' % (y0 + 10), '10mil')
    elif style == STYLE_DENT:
        # dent
        line('%dmil' % x0, '%dmil' % y0,
             '%dmil' % (width / 2 - 50), '%dmil' % y0, '10mil')
        arc('%dmil' % (width / 2), '%dmil' % y0, '50mil', '50mil', 0, 90, '10mil')
        arc('%dmil' % (width / 2), '%dmil' % y0, '50mil', '50mil', 90, 90, '10mil')
        line('%dmil' % (width / 2 + 50), '%dmil' % y0,
             '%dmil' % x1, '%dmil' % y0, '10mil')
    elif style == STYLE_BOXED:
        # box around pin 1
        line('%dmil' % x0, '%dmil' % y0, '%dmil' % x1, '%dmil' % y0, '10mil')
        line('-50mil', '50mil', '50mil', '50mil', '10mil')
        line('50mil', '-50mil', '50mil', '50mil', '10mil')
    elif style == STYLE_WSL_ARROW:
        # arrow
        line('%dmil' % x0, '%dmil' % y0, '%dmil' % x1, '%dmil' % y0, '10mil')
        line('-125mil', '50mil', '-75mil', '0mil', '10mil')
        line('-75mil', '0mil', '-125mil', '-50mil', '10mil')
    elif style == STYLE_WSL_DENT:
        # dent
        line('%dmil' % x0, '%dmil' % y0, '%dmil' % x1, '%dmil' % y0, '10mil')
        line('%dmil' % x0, '%dmil' % (height / 2 - 100),
             '%dmil' % (x0 + 50), '%dmil' % (height / 2 - 100), '10mil')
        line('%dmil' % (x0 + 50), '%dmil' % (height / 2 - 100),
             '%dmil' % (x0 + 50), '%dmil' % (height / 2 + 100), '10mil')
        line('%dmil' % (x0 + 50), '%dmil' % (height / 2 + 100),
             '%dmil' % x0, '%dmil' % (height / 2 + 100), '10mil')
    elif style == STYLE_PSL:
        # bottom part
        pin('50mil', '%dmil' % (height + 231.10),
            '147.80mil', '121.37mil', '151.74mil', '118.11mil', 0)
        line('299.21mil', '%dmil' % (height + 427.75),
             '929.13mil', '%dmil' % (height + 683.66), '10.00mil')
        line('653.54mil', '%dmil' % (height + 408.07),
             '968.50mil', '%dmil' % (height + 604.92), '10.00mil')
        line('653.54mil', '%dmil' % (height + 152.16),
             '456.69mil', '%dmil' % (height + 152.16), '10.00mil')
        line('653.54mil', '%dmil' % (height + 408.07),
             '653.54mil', '%dmil' % (height + 152.16), '10.00mil')
        line('220.47mil', '%dmil' % (height + 427.76),
             '653.54mil', '%dmil' % (height + 408.07), '10.00mil')
        line('870.079mil', '%dmil' % (height + 486.80),
             '850.40mil', '%dmil' % (height + 526.17), '10.00mil')
        line('889.77mil', '%dmil' % (height + 427.75),
             '870.079mil', '%dmil' % (height + 486.80), '10.00mil')
        line('988.189mil', '%dmil' % (height + 506.49),
             '889.77mil', '%dmil' % (height + 427.75), '10.00mil')
        line('50mil', '%dmil' % (height + 216.10),
             '50mil', '%dmil' % (height + 246.10), '10.00mil')
        line('35.00mil', '%dmil' % (height + 231.10),
             '65.00mil', '%dmil' % (height + 231.10), '10.00mil')
        line('988.189mil', '%dmil' % (height + 624.60),
             '988.189mil', '%dmil' % (height + 506.49), '10.00mil')
        line('988.189mil', '%dmil' % (height + 624.60),
             '968.50mil', '%dmil' % (height + 604.92), '10.00mil')
        arc('50mil', '%dmil' % (height + 231.10),
            '125.00mil', '125.00mil', 35, 290, '10.00mil')
        arc('929.13mil', '%dmil' % (height + 624.60),
            '59.06mil', '59.06mil', 90, 90, '10.00mil')

        # top part
        pin('50mil', '-231.10mil', '147.80mil', '123.37mil', '151.74mil', '118.11mil', 0)
        line('299.21mil', '-427.75mil', '929.13mil', '-683.66mil', '10.00mil')
        line('653.54mil', '-408.07mil', '968.50mil', '-604.92mil', '10.00mil')
        line('653.54mil', '-152.16mil', '456.69mil', '-152.16mil', '10.00mil')
        line('653.54mil', '-408.07mil', '653.54mil', '-152.16mil', '10.00mil')
        line('220.47mil', '-427.76mil', '653.54mil', '-408.07mil', '10.00mil')
        line('870.079mil', '-486.80mil', '850.40mil', '-526.17mil', '10.00mil')
        line('889.77mil', '-427.75mil', '870.079mil', '-486.80mil', '10.00mil')
        line('988.189mil', '-506.49mil', '889.77mil', '-427.75mil', '10.00mil')
        line('50mil', '-216.10mil', '50mil', '-246.10mil', '10.00mil')
        line('35.00mil', '-231.10mil', '65.00mil', '-231.10mil', '10.00mil')
        line('988.189mil', '-624.60mil', '988.189mil', '-506.49mil', '10.00mil')
        line('988.189mil', '-624.60mil', '968.50mil', '-604.92mil', '10.00mil')
        arc('50mil', '-231.10mil', '125.00mil', '125.00mil', 35, 290, '10.00mil')
        arc('929.13mil', '-624.60mil', '59.06mil', '59.06mil', 180, 90, '10.00mil')

        # box
        line('-55.12mil', '%dmil' % (height + 428.15),
             '259.84mil', '%dmil' % (height + 428.15), '10.00mil')
        line('-55.12mil', '-427.76mil', '-55.12mil',
             '%dmil' % (height + 428.15), '10.00mil')
        line('456.69mil', '%dmil' % (height + 418.32),
             '456.69mil', '-417.91mil', '10.00mil')
        line('220.47mil', '-427.76mil',
             '-55.12mil', '-427.76mil', '10.00mil')

        # mark on the left
        line('-75.00mil', '0mil', '-125.00mil', '-50.00mil', '10.00mil')
        line('-125.00mil', '50.00mil', '-75.00mil', '0mil', '10.00mil')

        # mark in the middle
        line('50mil', '%dmil' % (height / 2 - 50),
             '50mil', '%dmil' % (height / 2), '10.00mil')
        line('50mil', '%dmil' % (height / 2),
             '100.00mil', '%dmil' % (height / 2), '10.00mil')
        line('50mil', '%dmil' % (height / 2 + 50),
             '50mil', '%dmil' % (height / 2), '10.00mil')
        line('50mil', '%dmil' % (height / 2),
             '0mil', '%dmil' % (height / 2), '10.00mil')
    else:
        raise ValueError

    if style != STYLE_PSL:
        line('%dmil' % x1, '%dmil' % y0, '%dmil' % x1, '%dmil' % y1, '10mil')
        line('%dmil' % x1, '%dmil' % y1, '%dmil' % x0, '%dmil' % y1, '10mil')
        line('%dmil' % x0, '%dmil' % y1, '%dmil' % x0, '%dmil' % y0, '10mil')

    end()

if __name__ == '__main__':
    main()
