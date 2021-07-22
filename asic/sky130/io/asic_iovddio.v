module asic_iovddio #( 
    parameter DIR = "NO",
    parameter TYPE = "SOFT"
) (
    inout vdd,
    inout vss,
    inout vddio,
    inout vssio,
    inout poc
);

sky130_ef_io__vddio_hvc_pad vddio (
    // TODO: what do we connect these to?
    .DRN_HVC(),
    .SRC_BDY_HVC(),

    .VDDIO(vddio),
    .VDDIO_Q(vdd),
    .VDDA(vddio),
    .VCCD(vdd),
    .VSWITCH(vddio),
    .VCCHIB(vdd),
    .VSSA(vssio),
    .VSSD(vss),
    .VSSIO_Q(vss),
    .VSSIO(vssio),

    .AMXBUS_A(),
    .AMXBUS_B()
);

endmodule