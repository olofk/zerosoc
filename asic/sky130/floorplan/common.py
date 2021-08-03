import math

def floorplan_dims(fp):
    gpio_w = fp.available_cells['gpio'].width
    gpio_h = fp.available_cells['gpio'].height
    corner_w = fp.available_cells['corner'].width
    corner_h = fp.available_cells['corner'].height

    place_w = 6750 * fp.std_cell_width
    place_h = 900 * fp.std_cell_height
    margin_min = 100

    core_w = place_w + 2 * margin_min
    core_h = place_h + 2 * margin_min
    
    die_w = math.ceil(core_w + 2 * gpio_h) 
    die_h = math.ceil(core_h + 2 * gpio_h)

    # We recalculate core_w based on ceil'd die dimensions, essentially
    # "stretching" the core margin to ensure the die dimensions are integers
    core_w = die_w - 2 * gpio_h
    core_h = die_h - 2 * gpio_h

    we_io = [('gpio', i)  for i in range(5)] + [('clk', None), ('rstn', None), ('uart_rx', None), ('uart_tx', None)]
    n = len(we_io)
    spacing = (die_h - corner_h - corner_w - n * gpio_w) // (n + 1)

    y = corner_h + spacing
    we_pads = []
    for name, num in we_io:
        we_pads.append((name, num, y))
        y += gpio_w + spacing

    no_io = [('gpio', i) for i in range(5, 14)]
    n = len(no_io)
    spacing = (die_w - corner_h - corner_w - n * gpio_w) // (n + 1)

    x = corner_h + spacing
    no_pads = []
    for name, num in no_io:
        no_pads.append((name, num, x))
        x += gpio_w + spacing

    ea_io = [('gpio', i) for i in range(14, 23)]
    n = len(ea_io)
    spacing = (die_h - corner_h - corner_w - n * gpio_w) // (n + 1)

    y = corner_w + spacing
    ea_pads = []
    for name, num in ea_io:
        ea_pads.append((name, num, y))
        y += gpio_w + spacing

    so_io = [('gpio', i) for i in range(23, 32)]
    n = len(so_io)
    spacing = (die_w - corner_h - corner_w - n * gpio_w) // (n + 1)

    x = corner_w + spacing
    so_pads = []
    for name, num in so_io:
        so_pads.append((name, num, x))
        x += gpio_w + spacing

    return die_w, die_h, core_w, core_h, place_w, place_h, we_pads, no_pads, ea_pads, so_pads