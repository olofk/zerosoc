# Bit of a hack to be able to import 'common' when dynamically importing this
# module. TODO: cleaner way to handle this?
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from common import *

def setup_floorplan(fp, chip):
    # TODO: this should be automatically set to a valid value
    fp.db_units = 1000

    _, _, die_w, die_h, core_w, core_h, we_pads, no_pads, ea_pads, so_pads = floorplan_dims(fp)
    
    gpio_w = fp.available_cells['gpio'].width
    gpio_h = fp.available_cells['gpio'].height
    ram_w = fp.available_cells['ram'].width
    ram_h = fp.available_cells['ram'].height

    margin_w = (die_w - core_w) / 2
    margin_h = (die_h - core_h) / 2

    ram_core_space = 250 * fp.std_cell_width

    ram_x = fp.snap(die_w - margin_w - ram_w - ram_core_space, fp.std_cell_width)
    ram_y = fp.snap(die_h - margin_h - ram_h - 50 * fp.std_cell_height, fp.std_cell_height)
    
    fp.create_die_area(die_w, die_h, core_area = (margin_w, margin_h, ram_x - ram_core_space, core_h + margin_h))
    
    # Place RAM
    # Must be placed outside core area to ensure we don't run into routing
    # congestion issues (due to cells being placed too close to RAM pins)
    fp.place_macros([('ram.u_mem.gen_sky130.u_impl_sky130.genblk1.mem', 'ram')], ram_x, ram_y, 0, 0, 'N')

    # Place pins
    oe_offset = 4.245
    out_offset = 19.885
    in_offset = 75.08
    pin_width = 0.28
    pin_depth = 1

    for name, num, y in we_pads:
        oe_pin = f'{name}_en_o' + (f'[{num}]' if num is not None else '')
        out_pin = f'{name}_o' + (f'[{num}]' if num is not None else '')
        in_pin = f'{name}_i' + (f'[{num}]' if num is not None else '')

        y -= gpio_h

        fp.place_pins([oe_pin], 0, y + oe_offset, 0, 0, pin_depth, pin_width, 'm2')
        fp.place_pins([out_pin], 0, y + out_offset, 0, 0, pin_depth, pin_width, 'm2')
        fp.place_pins([in_pin], 0, y + in_offset, 0, 0, pin_depth, pin_width, 'm2')

    for name, num, x in no_pads:
        oe_pin = f'{name}_en_o' + (f'[{num}]' if num is not None else '')
        out_pin = f'{name}_o' + (f'[{num}]' if num is not None else '')
        in_pin = f'{name}_i' + (f'[{num}]' if num is not None else '')

        x -= gpio_h

        fp.place_pins([oe_pin], x + oe_offset, die_h - pin_depth, 0, 0, pin_width, pin_depth, 'm2')
        fp.place_pins([out_pin], x + out_offset, die_h - pin_depth, 0, 0, pin_width, pin_depth, 'm2')
        fp.place_pins([in_pin], x + in_offset, die_h - pin_depth, 0, 0, pin_width, pin_depth, 'm2')

    for name, num, y in ea_pads:
        oe_pin = f'{name}_en_o' + (f'[{num}]' if num is not None else '')
        out_pin = f'{name}_o' + (f'[{num}]' if num is not None else '')
        in_pin = f'{name}_i' + (f'[{num}]' if num is not None else '')

        y -= gpio_h 

        fp.place_pins([oe_pin], die_w - pin_depth, y + gpio_w - oe_offset - pin_width, 0, 0, pin_depth, pin_width, 'm2')
        fp.place_pins([out_pin], die_w - pin_depth, y + gpio_w - out_offset - pin_width, 0, 0, pin_depth, pin_width, 'm2')
        fp.place_pins([in_pin], die_w - pin_depth, y + gpio_w - in_offset - pin_width, 0, 0, pin_depth, pin_width, 'm2')

    for name, num, x in so_pads:
        oe_pin = f'{name}_en_o' + (f'[{num}]' if num is not None else '')
        out_pin = f'{name}_o' + (f'[{num}]' if num is not None else '')
        in_pin = f'{name}_i' + (f'[{num}]' if num is not None else '')

        x -= gpio_h

        fp.place_pins([oe_pin], x + gpio_w - oe_offset - pin_width, 0, 0, 0, pin_width, pin_depth, 'm2')
        fp.place_pins([out_pin], x + gpio_w - out_offset - pin_width, 0, 0, 0, pin_width, pin_depth, 'm2')
        fp.place_pins([in_pin], x + gpio_w - in_offset - pin_width, 0, 0, 0, pin_width, pin_depth, 'm2')
    
    return fp
