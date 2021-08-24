from siliconcompiler.core import Chip
from siliconcompiler.floorplan import Floorplan

import math

def configure_chip(design):
    chip = Chip()
    chip.target('skywater130')
    chip.set('design', design)

    libname = 'ram'
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'type', 'component')
    chip.add('library', libname, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    chip.add('library', libname, 'lef', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    chip.add('library', libname, 'gds', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds')
    chip.set('library', libname, 'cells', 'ram', 'sky130_sram_2kbyte_1rw1r_32x512_8')

    libname = 'io'
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'type', 'component')
    chip.add('library', libname, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/io/sky130_dummy_io.lib')
    chip.set('library', libname, 'lef', 'asic/sky130/io/sky130_ef_io.lef')
    # Need both GDS files: ef relies on fd one
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_ef_io.gds')
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_fd_io.gds')
    chip.set('library', libname, 'cells', 'gpio', 'sky130_ef_io__gpiov2_pad')
    chip.set('library', libname, 'cells', 'vdd', 'sky130_ef_io__vccd_hvc_pad')
    chip.set('library', libname, 'cells', 'vddio', 'sky130_ef_io__vddio_hvc_pad')
    chip.set('library', libname, 'cells', 'vss', 'sky130_ef_io__vssd_hvc_pad')
    chip.set('library', libname, 'cells', 'vssio', 'sky130_ef_io__vssio_hvc_pad')
    chip.set('library', libname, 'cells', 'corner', 'sky130_ef_io__corner_pad')
    chip.set('library', libname, 'cells', 'fill1',  'sky130_ef_io__com_bus_slice_1um')
    chip.set('library', libname, 'cells', 'fill5',  'sky130_ef_io__com_bus_slice_5um')
    chip.set('library', libname, 'cells', 'fill10', 'sky130_ef_io__com_bus_slice_10um')
    chip.set('library', libname, 'cells', 'fill20', 'sky130_ef_io__com_bus_slice_20um')

    return chip

def core_floorplan(fp):
    ## SECTION 1 ##

    # Specify area as multiples of standard cell size
    core_w = 6750 * fp.std_cell_width
    core_h = 900 * fp.std_cell_height
    margin_x = 150 * fp.std_cell_width
    margin_y = 25 * fp.std_cell_height
    # Die dimensions must be whole number in order to be filled by I/O fill cells
    die_w = math.ceil(core_w + 2 * margin_x)
    die_h = math.ceil(core_h + 2 * margin_y)
    # Create die_area 
    fp.create_die_area(die_w, die_h, core_area=(margin_x, margin_y, margin_x + core_w, margin_y + core_h))
    ## END SECTION 1 ##

    ## SECTION 2 ##
    # Place macro
    ram_w = fp.available_cells['ram'].width
    ram_h = fp.available_cells['ram'].height
    ram_x = margin_x + core_w - ram_w
    ram_y = margin_y + core_h - ram_h
    fp.place_macros([('soc.ram.u_mem.gen_sky130.u_impl_sky130.genblk1.mem', 'ram')], ram_x, ram_y, 0, 0, 'N', snap=True)
    # Calculated empirically
    ram_core_space_x = 240 * fp.std_cell_width
    ram_core_space_y = 60 * fp.std_cell_height
    # Place blockage
    # fp.place_blockage(ram_x - ram_core_space_x, ram_y - ram_core_space_y,
    #     ram_w + 2 * ram_core_space_x, ram_h + 2 * ram_core_space_y)
    ## END SECTION 2 ##

    ## SECTION 3 ##
    # Place pins
    pin_depth = 1

    pins = [
        # Hack: tweak these two pin sizes to trick router and avoid DRC errors
        ('tech_cfg', 5, 16, 78.580 - 1, 78.910, 'm3'), # enable_vddio
        ('din', 0, 1, 79.240, 79.570 + 1, 'm3'), # in

        ('dout', 0, 1, 22.355, 22.615, 'm2'), # out
        ('ie', 0, 1, 45.245, 45.505, 'm2'), # inp_dis
        ('oen', 0, 1, 3.375, 3.605, 'm2'), # oe_n
        ('tech_cfg', 0, 16, 31.815, 32.075, 'm2'), # hld_h_n
        ('tech_cfg', 1, 16, 35.460, 35.720, 'm2'), # enable_h
        ('tech_cfg', 2, 16, 38.390, 38.650, 'm2'), # enable_inp_h
        ('tech_cfg', 3, 16, 12.755, 13.015, 'm2'), # enable_vdda_h
        ('tech_cfg', 4, 16, 16.310, 16.570, 'm2'), # enable_vswitch_h
        ('tech_cfg', 6, 16, 5.420, 5.650, 'm2'), # ib_mode_sel
        ('tech_cfg', 7, 16, 6.130, 6.390, 'm2'), # vtrip_sel
        ('tech_cfg', 8, 16, 77.610, 77.870, 'm2'), # slow
        ('tech_cfg', 9, 16, 26.600, 26.860, 'm2'), # hld_ovr
        ('tech_cfg', 10, 16, 62.430, 62.690, 'm1'), # analog_en
        ('tech_cfg', 11, 16, 30.750, 31.010, 'm2'), # analog_sel
        ('tech_cfg', 12, 16, 45.865, 46.195, 'm3'), # analog_pol
        ('tech_cfg', 13, 16, 49.855, 50.115, 'm2'), # dm[0]
        ('tech_cfg', 14, 16, 66.835, 67.095, 'm2'), # dm[1]
        ('tech_cfg', 15, 16, 28.490, 28.750, 'm2'), # dm[2]
    ]

    i = 0
    for pad_type, y in we_pads:
        y -= gpio_h
        if pad_type == 'gpio':
            for pin, bit, width, offset_l, offset_h, layer in pins:
                name = f'we_{pin}[{i * width + bit}]'
                pin_width = offset_h - offset_l
                fp.place_pins([name], 0, y + offset_l, 0, 0, pin_depth, pin_width, layer)
            i += 1

    i = 0
    for pad_type, x in no_pads:
        x -= gpio_h
        if pad_type == 'gpio':
            for pin, bit, width, offset_l, offset_h, layer in pins:
                name = f'no_{pin}[{i * width + bit}]'
                pin_width = offset_h - offset_l
                fp.place_pins([name], x + offset_l, die_h - pin_depth, 0, 0, pin_width, pin_depth, layer)
            i += 1

    i = 0
    for pad_type, y in ea_pads:
        y -= gpio_h
        if pad_type == 'gpio':
            for pin, bit, width, offset_l, offset_h, layer in pins:
                name = f'ea_{pin}[{i * width + bit}]'
                pin_width = offset_h - offset_l
                fp.place_pins([name], die_w - pin_depth, y + gpio_w - offset_l - pin_width, 0, 0, pin_depth, pin_width, layer)
            i += 1

    i = 0
    for pad_type, x in so_pads:
        x -= gpio_h
        if pad_type == 'gpio':
            for pin, bit, width, offset_l, offset_h, layer in pins:
                name = f'so_{pin}[{i * width + bit}]'
                pin_width = offset_h - offset_l
                fp.place_pins([name], x + gpio_w - offset_l - pin_width, 0, 0, 0, pin_width, pin_depth, layer)
            i += 1
    ## END SECTION 3 ##


if __name__ == '__main__':
    chip = configure_chip('asic_core')
    fp = Floorplan(chip)
    core_floorplan(fp)
    fp.write_def('asic_core.def')
    fp.write_lef('asic_core.lef')

    chip = configure_chip('asic_top')
    fp = Floorplan(chip)
    top_floorplan(fp)
    fp.write_def('asic_top.def')
