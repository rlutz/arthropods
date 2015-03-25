#!/usr/bin/python
import getopt, sys
from fpgen import *

pin_thickness = 1.5 # mm
pin_clearance = 1. # mm
pin_mask = 1.6 # mm
pin_drill = 1. # mm

pad_thickness = 1.492 # mm
pad_clearance = 1. # mm
pad_mask = 1.59 # mm

SIP, DIP, DIPwide, ONEPIN, TWOPIN, TWOPIN_WSL, TWOPIN_WSLalt = xrange(7)
variant_map = { 'SIP': SIP, 'DIP': DIP, 'DIPwide': DIPwide,
                '1xPIN': ONEPIN, '2xPIN': TWOPIN,
                'WSL': TWOPIN_WSL, 'WSLalt': TWOPIN_WSLalt }

def invalid_arguments(message):
    sys.stderr.write("%s: %s\n" % (sys.argv[0], message))
    sys.stderr.write("Try `%s --help' for more information.\n" % sys.argv[0])
    sys.exit(1)

def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:], '', ['help', 'version'])
    except getopt.GetoptError as e:
        invalid_arguments(e.msg)

    for option, value in options:
        if option == '--help':
            sys.stdout.write("Usage: %s VARIANT PIN_COUNT\n" % sys.argv[0])
            sys.stdout.write("\n")
            sys.stdout.write(
"      --help            give this help\n"
"      --version         display version number\n")
            sys.stdout.write("\n")
            sys.stdout.write("Supported variants: %s\n" %
                             ', '.join(sorted(variant_map.keys())))
            sys.exit(0)
        elif option == '--version':
            xorn.command.core_version()
        else:
            raise AssertionError

    try:
        variant_str, pin_count_str = args
    except ValueError:
        sys.stdout.write("Usage: %s VARIANT PIN_COUNT\n" % sys.argv[0])
        sys.stderr.write("Try `%s --help' for more information.\n"
                         % sys.argv[0])
        sys.exit(1)

    try:
        variant = variant_map[variant_str]
    except KeyError:
        invalid_arguments("`%s' is not a valid variant" % variant_str)

    try:
        pin_count = int(pin_count_str)
    except ValueError:
        invalid_arguments("`%s' is not an integer" % pin_count_str)

    if variant == SIP:
        rows = 1
        eff_pin_count = pin_count
    elif variant in [DIP, DIPwide]:
        if pin_count % 2 != 0:
            invalid_arguments("DIP pin count must be even")
        rows = 2
        eff_pin_count = pin_count // rows
    elif variant == ONEPIN:
        rows = 1
        eff_pin_count = pin_count
    elif variant in [TWOPIN, TWOPIN_WSL, TWOPIN_WSLalt]:
        rows = 2
        eff_pin_count = pin_count
    else:
        raise AssertionError

    text_x, text_y, text_dir, text_scale, text_format = {
        SIP: ('120mil', '-45mil', 3, 100, 'SIP%d'),
        DIP: ('180mil', '25mil', 3, 100, 'DIP%d'),
        DIPwide: ('330mil', '25mil', 3, 100, 'DIP%d'),
        ONEPIN: ('120mil', '-45mil', 3, 100, '1x%dPIN'),
        TWOPIN: ('-50mil', '-120mil', 0, 100, '2x%dPIN'),
        TWOPIN_WSL: ('-125mil', '-270mil', 0, 100, '2x%dPIN'),
        TWOPIN_WSLalt: ('-125mil', '-270mil', 0, 100, '2x%dPIN')
    }[variant]
    desc = text_format % pin_count

    start(None, desc, desc, desc, 0., 0.,
          text_x, text_y, text_dir, text_scale, None)

    for i in xrange(0, eff_pin_count):
        y = '%dmil' % (i * 100)
        if i == 0:
            maybe_square = ['square']
        else:
            maybe_square = []

        if variant == SIP:
            pin(0., y, pin_thickness, pin_clearance, pin_mask, pin_drill,
                i + 1, flags = maybe_square)
            pad('-25mil', y, '25mil', y,
                pad_thickness, pad_clearance, pad_mask,
                i + 1, flags = ['onsolder'] + maybe_square)
        elif variant in [DIP, DIPwide]:
            if variant == DIPwide:
                width = 600.
            else:
                width = 300.
            pin(  '0mil', y, pin_thickness, pin_clearance, pin_mask, pin_drill,
                i + 1, flags = maybe_square)
            pad('-25mil', y, '25mil', y,
                pad_thickness, pad_clearance, pad_mask,
                i + 1, flags = ['onsolder'] + maybe_square)
            pin('%dmil' % width, y,
                pin_thickness, pin_clearance, pin_mask, pin_drill,
                pin_count - i)
            pad('%dmil' % (width - 25.), y, '%dmil' % (width + 25.), y,
                pad_thickness, pad_clearance, pad_mask,
                pin_count - i, flags = ['onsolder', 'edge2'])
        elif variant == ONEPIN:
            pin(0., y, pin_thickness, pin_clearance, pin_mask, pin_drill,
                i + 1, flags = maybe_square)
            pad('-25mil', y, '25mil', y,
                pad_thickness, pad_clearance, pad_mask,
                i + 1, flags = ['onsolder'] + maybe_square)
        elif variant in [TWOPIN, TWOPIN_WSL, TWOPIN_WSLalt]:
            pin(  '0mil', y, pin_thickness, pin_clearance, pin_mask, pin_drill,
                i * 2 + 1, flags = maybe_square)
            pin('100mil', y, pin_thickness, pin_clearance, pin_mask, pin_drill,
                i * 2 + 2)
            pad('-50mil', y, '0mil', y,
                pad_thickness, pad_clearance, pad_mask,
                i * 2 + 1, flags = ['onsolder'] + maybe_square)
            pad('100mil', y, '150mil', y,
                pad_thickness, pad_clearance, pad_mask,
                i * 2 + 2, flags = ['onsolder', 'edge2'])
        else:
            raise AssertionError

    # Paint outline

    x_offset = 50
    y_offset = 50

    if variant == SIP:
        width = 0
    elif variant == DIP:
        width = 300
    elif variant == DIPwide:
        width = 600
    elif variant == ONEPIN:
        width = 0
    elif variant == TWOPIN:
        width = 100
    elif variant in [TWOPIN_WSL, TWOPIN_WSLalt]:
        width = 100
        x_offset = 125
        y_offset = 200
    else:
        raise AssertionError

    height = (eff_pin_count - 1) * 100

    x0 = -x_offset; x1 = width + x_offset
    y0 = -y_offset; y1 = height + y_offset

    if variant == SIP:
        # thick line
        line('%dmil' % x0, '%dmil' % y0,
             '%dmil' % x1, '%dmil' % y0, '10mil')
        line('%dmil' % x0, '%dmil' % (y0 + 5),
             '%dmil' % x1, '%dmil' % (y0 + 5), '10mil')
        line('%dmil' % x0, '%dmil' % (y0 + 10),
             '%dmil' % x1, '%dmil' % (y0 + 10), '10mil')
    elif variant in [DIP, DIPwide]:
        # dent
        line('%dmil' % x0, '%dmil' % y0,
             '%dmil' % (width / 2 - 50), '%dmil' % y0, '10mil')
        arc('%dmil' % (width / 2), '%dmil' % y0, '50mil', '50mil', 0, 90, '10mil')
        arc('%dmil' % (width / 2), '%dmil' % y0, '50mil', '50mil', 90, 90, '10mil')
        line('%dmil' % (width / 2 + 50), '%dmil' % y0,
             '%dmil' % x1, '%dmil' % y0, '10mil')
    elif variant == TWOPIN:
        # box around pin 1
        line('%dmil' % x0, '%dmil' % y0, '%dmil' % x1, '%dmil' % y0, '10mil')
        line('-50mil', '50mil', '50mil', '50mil', '10mil')
        line('50mil', '-50mil', '50mil', '50mil', '10mil')
    elif variant == TWOPIN_WSL:
        # arrow
        line('%dmil' % x0, '%dmil' % y0, '%dmil' % x1, '%dmil' % y0, '10mil')
        line('-125mil', '50mil', '-75mil', '0mil', '10mil')
        line('-75mil', '0mil', '-125mil', '-50mil', '10mil')
    elif variant == TWOPIN_WSLalt:
        # dent
        line('%dmil' % x0, '%dmil' % y0, '%dmil' % x1, '%dmil' % y0, '10mil')
        line('%dmil' % x0, '%dmil' % (height / 2 - 100),
             '%dmil' % (x0 + 50), '%dmil' % (height / 2 - 100), '10mil')
        line('%dmil' % (x0 + 50), '%dmil' % (height / 2 - 100),
             '%dmil' % (x0 + 50), '%dmil' % (height / 2 + 100), '10mil')
        line('%dmil' % (x0 + 50), '%dmil' % (height / 2 + 100),
             '%dmil' % x0, '%dmil' % (height / 2 + 100), '10mil')
    else:
        # nothing special here
        line('%dmil' % x0, '%dmil' % y0, '%dmil' % x1, '%dmil' % y0, '10mil')

    line('%dmil' % x1, '%dmil' % y0, '%dmil' % x1, '%dmil' % y1, '10mil')
    line('%dmil' % x1, '%dmil' % y1, '%dmil' % x0, '%dmil' % y1, '10mil')
    line('%dmil' % x0, '%dmil' % y1, '%dmil' % x0, '%dmil' % y0, '10mil')

    end()

if __name__ == '__main__':
    main()
