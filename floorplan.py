from siliconcompiler.core import Chip
from siliconcompiler.floorplan import Floorplan

import math

def configure_chip(design):
  chip = Chip()
  chip.target('skywater130')

  chip.set('design', design)

  libname = 'ram'
  chip.add('library', libname, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
  chip.add('library', libname, 'lef', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
  chip.add('library', libname, 'gds', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds')
  chip.set('library', libname, 'cells', 'ram', 'sky130_sram_2kbyte_1rw1r_32x512_8')
  chip.add('asic', 'macrolib', libname)
  chip.set('library', libname, 'type', 'component')

  libname = 'io'
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
  chip.add('asic', 'macrolib', libname)
  chip.set('library', libname, 'type', 'component')

  return chip

def define_dimensions(fp):
  place_w = 6750 * fp.std_cell_width
  place_h = 900 * fp.std_cell_height
  margin_left = 150 * fp.std_cell_width
  margin_bottom = 25 * fp.std_cell_height

  core_w = math.ceil(place_w + 2 * margin_left)
  core_h = math.ceil(place_h + 2 * margin_bottom)
  gpio_h = fp.available_cells['gpio'].height + 2.035
  top_w = core_w + 2 * gpio_h
  top_h = core_h + 2 * gpio_h
  
  return (top_w, top_h), (core_w, core_h), (place_w, place_h), (margin_left, margin_bottom)

def core_floorplan(fp):
  _, (core_w, core_h), (place_w, place_h), (margin_left, margin_bottom) = define_dimensions(fp)
  fp.create_die_area(core_w, core_h, core_area=(margin_left, margin_bottom, place_w + margin_left, place_h + margin_bottom))

def main():
  core_chip = configure_chip('asic_core')
  core_fp = Floorplan(core_chip)
  core_floorplan(core_fp)
  core_fp.write_def('asic_core.def')

if __name__ == '__main__':
  main()