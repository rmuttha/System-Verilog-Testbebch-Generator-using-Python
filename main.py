# System Verilog Testbench Generator
# 
# This script generates a testbench for System Verilog hardware designs. 
# It automates the creation of testbenches, including stimulus generation, 
# output monitoring, and simulation setup. The testbench generated by this 
# script can be used to verify the functionality of the design under test (DUT).
#
# Author: Rutuja Muttha & Tanmay Mhetre
# Date: May 23, 2024
#
# Usage:
# 1. Place the System Verilog file (file.sv) in the specified path.
# 2. Run this script.
# 3. The script will parse the System Verilog file, generate test vectors, 
#    monitor outputs, and create a testbench.
# 4. The generated testbench will be saved in the same directory as the System 
#    Verilog file with the name 'generated_testbench.sv'.
# 5. Load the generated testbench in a simulation tool (e.g., QuestaSim) and 
#    run the simulation.
#
# Note: Ensure the System Verilog file is correctly formatted and includes 
#       necessary module definitions, input/output declarations, and 
#       parameters.


import os
import re

# Set of reserved keywords in System Verilog
RESERVED_KEYWORDS = {
    "always", "and", "assign", "automatic", "begin", "buf", "bufif0", "bufif1", "case", "casex", "casez", "cmos",
    "deassign", "default", "defparam", "disable", "edge", "else", "end", "endcase", "endfunction", "endgenerate",
    "endmodule", "endprimitive", "endspecify", "endtable", "endtask", "event", "for", "force", "forever", "fork",
    "function", "generate", "genvar", "highz0", "highz1", "if", "initial", "inout", "input", "integer", "join", 
    "large", "macromodule", "medium", "module", "nand", "negedge", "nmos", "nor", "not", "notif0", "notif1", "or", 
    "output", "parameter", "pmos", "posedge", "primitive", "pull0", "pull1", "pulldown", "pullup", "rcmos", 
    "reg", "release", "repeat", "rnmos", "rpmos", "rtran", "rtranif0", "rtranif1", "scalared", "signed", "small", 
    "specify", "specparam", "strong0", "strong1", "supply0", "supply1", "table", "task", "time", "tran", 
    "tranif0", "tranif1", "tri", "tri0", "tri1", "triand", "trior", "trireg", "unsigned", "vectored", "wait", 
    "wand", "weak0", "weak1", "while", "wire", "wor", "xnor", "xor"
}


def sanitize_signal_name(signal_name):
    """
    Sanitizes a signal name to ensure it does not clash with reserved keywords.
    Appends '_sig' if the signal name is a reserved keyword.
    """
    if signal_name in RESERVED_KEYWORDS:
        return signal_name + "_sig"
    return signal_name

def parse_system_verilog(filepath):
    """
    Parses a System Verilog file and returns a representation of the design.
    Parameters:
    filepath (str): The path to the System Verilog file.
    Returns:
    dict: A dictionary representation of the design containing modules, signals, and parameters.
    """
    design = {
        'modules': [],
        'signals': [],
        'parameters': []
    }
    # Read the file content
    try:
        with open(filepath, 'r', encoding='utf-16') as file:
            content = file.read()
    except UnicodeError:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return design
    except Exception as e:
        print(f"Error reading file: {e}")
        return design

    # Debug: Print the file content
    print(f"File content:\n{content}\n")

    # Enhanced regex-based parsing for modules, signals, and parameters
    modules = re.findall(r'\bmodule\s+(\w+)\s*\(', content, re.IGNORECASE)
    signals = re.findall(r'\b(input|output|inout)\s+(?:wire|reg|logic)?\s*(\[.*?\])?\s*(\w+)', content, re.IGNORECASE)
    parameters = re.findall(r'\bparameter\s+(\w+)\s*=\s*([\w\'\[\]:]+);', content, re.IGNORECASE)

    # Debug: Print parsed items
    print(f"Parsed modules: {modules}")
    print(f"Parsed signals: {signals}")
    print(f"Parsed parameters: {parameters}")

    design['modules'] = modules
    design['signals'] = [(s[0], s[1], sanitize_signal_name(s[2])) for s in signals if s[2] not in RESERVED_KEYWORDS]  # Filter out invalid signals
    design['parameters'] = [(p[0], p[1]) for p in parameters]  # Store parameter names and values

    return design


def generate_test_vectors(signals):
    """
    Generates test vectors for the design.
   
    Parameters:
    - signals: List of tuples representing the signals in the design.
    Returns:
    - A list of strings representing the test vectors for the testbench.
    """
    test_vectors = ["  initial begin"]
    test_vectors.append("    // Initialize inputs and apply test vectors")
    for signal_type, signal_width, signal_name in signals:
        if signal_type in ['input', 'inout']:
            test_vectors.append(f"    {signal_name} = 0;")
    test_vectors.append("    // Apply test vectors")
    test_vectors.append("    #10;")
    test_vectors.append("    res_n = 1;")
    test_vectors.append("    #10;")
    for signal_type, signal_width, signal_name in signals:
        if signal_type in ['input', 'inout'] and 'clk' in signal_name.lower():
            test_vectors.append(f"    forever #5 {signal_name} = ~{signal_name};")
    test_vectors.append("  end")
    return test_vectors

def monitor_output(signals):
    """
    Monitors the output of the design under test.
    Parameters:
    - signals: List of tuples representing the signals in the design.
    Returns:
    - A list of strings representing the monitor code for the testbench.
    """
    monitor_code = ["  initial begin"]
    monitor_code.append("    $monitor(\"At time %0t:")
    for signal_type, signal_width, signal_name in signals:
        monitor_code.append(f" {signal_name} = %b,")
    monitor_code[-1] = monitor_code[-1].rstrip(",")  # Remove trailing comma
    monitor_code.append("\", $time")
    for signal_type, signal_width, signal_name in signals:
        monitor_code.append(f", {signal_name}")
    monitor_code.append(");")
    monitor_code.append("  end")
    return monitor_code

def setup_simulation(modules, signals, test_vectors, monitor):
    """
    Sets up the simulation environment.
    Parameters:
    - modules: List of module names in the design.
    - signals: List of tuples representing the signals in the design.
    - test_vectors: List of strings representing the test vectors for the testbench.
    - monitor: List of strings representing the monitor code for the testbench.
    Returns:
    - A list of strings representing the complete testbench code.
    """
    simulation_code = ["`timescale 1ns / 1ps\n"]
    for module in modules:
        simulation_code.append(f"module {module}_tb;\n")
        simulation_code.append("  // Declare variables for the inputs and outputs of the DUT (Device Under Test)\n")
        for signal_type, signal_width, signal_name in signals:
            signal_type_decl = 'reg' if signal_type in ['input', 'inout'] else 'wire'
            if signal_width:
                signal_declaration = f"{signal_type_decl} {signal_width} {signal_name};"
            else:
                signal_declaration = f"{signal_type_decl} {signal_name};"
            simulation_code.append(f"  {signal_declaration}\n")
        simulation_code.append("\n  // Instantiate the DUT\n")
        simulation_code.append(f"  {module} uut (\n")
        for signal_type, signal_width, signal_name in signals:
            simulation_code.append(f"    .{signal_name}({signal_name}),\n")
        simulation_code[-1] = simulation_code[-1].rstrip(",\n") + "\n  );\n"
        simulation_code.append("\n  // Test vectors\n")
        simulation_code.extend(test_vectors)
        simulation_code.append("\n  // Monitor changes\n")
        simulation_code.extend(monitor)
        simulation_code.append("  initial begin\n    #200 $finish;\n  end\n")  # Stop simulation after 200 time units
        simulation_code.append("endmodule\n")
    return simulation_code

def save_testbench(output_dir, simulation_code):
    """
    Saves the generated testbench to a file.
    Parameters:
    output_dir (str): The directory to save the testbench file.
    simulation_code (list): List of strings representing the simulation setup code.
    Returns:
    str: The path to the saved testbench file.
    """
    tb_path = os.path.join(output_dir, 'generated_testbench.sv')
    with open(tb_path, 'w') as file:
        file.writelines("\n".join(simulation_code))  # Join with newline for better formatting
    return tb_path

def analyze_results():
    """
    Analyzes the results of the simulation.
    Returns:
    dict: Dictionary representing the analysis results with pass/fail status and failures list.
    """
    results = {
        'pass': True,
        'failures': []
    }
    return results

def main():
    """
    Main function to generate the testbench for the System Verilog design.
    """
    filepath = r'C:\Users\mutth\study\Final Project\system_verilog_testbench_generator\file.sv'
    output_dir = os.path.dirname(filepath)

    # Parse System Verilog files
    design = parse_system_verilog(filepath)

    # Check if design parsing was successful
    if not design['modules']:
        print("No modules found in the design. Exiting.")
        return

    # Generate test vectors
    test_vectors = generate_test_vectors(design['signals'])

    # Monitor outputs
    monitor = monitor_output(design['signals'])

    # Setup simulation
    simulation_code = setup_simulation(design['modules'], design['signals'], test_vectors, monitor)

    # Save the generated testbench
    tb_path = save_testbench(output_dir, simulation_code)
    print(f"Testbench generated and saved to: {tb_path}")

    # Execute simulation and analyze results
    results = analyze_results()
    print(results)

if __name__ == "__main__":
    main()
