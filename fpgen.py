def start(flags, desc, name, value, mark_x, mark_y,
          text_x, text_y, text_dir, text_scale, text_flags):
    if isinstance(flags, list):
        flags = ','.join(flags)
    elif flags is None:
        flags = ""
    if name is None:
        name = desc
    if value is None:
        value = desc
    if isinstance(text_flags, list):
        text_flags = ','.join(text_flags)
    elif text_flags is None:
        text_flags = ""
    print 'Element["%s" "%s" "%s" "%s" %s %s %s %s %s %s "%s"]' % (
        flags, desc, name, value,
        format(mark_x), format(mark_y), format(text_x), format(text_y),
        text_dir, text_scale, text_flags)
    print '('

def format_number(length, unit):
    if isinstance(length, str):
        if '.' in length:
            length = float(length)
        else:
            length = int(length)
    if isinstance(length, int):
        if length == 0:
            return "0.0000"
        return "%d.00%s" % (length, unit)
    if isinstance(length, float):
        if length == 0.:
            return "0.0000"
        if unit == 'mm':
            return "%.4f%s" % (length, unit)
        if unit == 'mil':
            return "%.2f%s" % (length, unit)
    raise ValueError

def format(length):
    if isinstance(length, int) or isinstance(length, float):
        return format_number(length, 'mm')
    if isinstance(length, str):
        if length.endswith("mm"):
            return format_number(length[:-2], length[-2:])
        if length.endswith("mil"):
            return format_number(length[:-3], length[-3:])
    raise ValueError

def pin(x, y, thickness, clearance, mask, drill,
        name, number = None, flags = None):
    if number is None:
        number = name
    if isinstance(flags, list):
        flags = ','.join(flags)
    elif flags is None:
        flags = ""
    print "\tPin[%s %s %s %s %s %s \"%s\" \"%s\" \"%s\"]" % (
        format(x), format(y),
        format(thickness), format(clearance), format(mask), format(drill),
        name, number, flags)

def pad(x0, y0, x1, y1, thickness, clearance, mask,
        name, number = None, flags = None):
    if number is None:
        number = name
    if isinstance(flags, list):
        flags = ','.join(flags)
    elif flags is None:
        flags = ""
    print "\tPad[%s %s %s %s %s %s %s \"%s\" \"%s\" \"%s\"]" % (
        format(x0), format(y0), format(x1), format(y1),
        format(thickness), format(clearance), format(mask),
        name, number, flags)

def line(x0, y0, x1, y1, thickness):
    print "\tElementLine [%s %s %s %s %s]" % (
        format(x0), format(y0), format(x1), format(y1), format(thickness))

def arc(x, y, xradius, yradius, start_angle, delta_angle, thickness):
    print "\tElementArc [%s %s %s %s %d %d %s]" % (
        format(x), format(y), format(xradius), format(yradius),
        start_angle, delta_angle, format(thickness))

def end():
    print
    print "\t)"
