def setup_simulation(design):
    """
    Sets up the simulation environment.
    """
    with open('simulation_setup.sv', 'w') as file:
        file.write("// Simulation Setup\n")
        file.write("`timescale 1ns/1ps\n")
        for module in design['modules']:
            file.write(f"module tb_{module};\n")
            file.write("  // DUT instantiation\n")
            file.write(f"  {module} dut ();\n")
            file.write("  // Add stimulus and monitor\n")
            file.write("endmodule\n")
