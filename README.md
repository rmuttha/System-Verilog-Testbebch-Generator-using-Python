# System Verilog Testbench Generator

## Overview

The System Verilog Testbench Generator is a Python script designed to automate the creation of testbenches for System Verilog hardware designs. This tool helps in streamlining the verification process by generating comprehensive testbenches, including stimulus generation, output monitoring, and simulation setup. The generated testbench can be used to verify the functionality of the design under test (DUT).

## Features

- **Automated Testbench Generation**: Automatically creates a testbench for System Verilog designs.
- **Stimulus Generation**: Generates random and predetermined test vectors for input signals.
- **Output Monitoring**: Includes code to monitor the outputs of the DUT during simulation.
- **Simulation Setup**: Prepares the simulation environment for tools like QuestaSim.
- **Simulation Control**: Stops the simulation after a predefined period.

## Prerequisites

- Python 3.x
- A System Verilog file with the design to be tested
- Simulation tool (e.g., QuestaSim) to run the generated testbench

## Usage

### Step 1: Prepare Your System Verilog File

Ensure your System Verilog file is correctly formatted and includes necessary module definitions, input/output declarations, and parameters. Place the file in the specified directory.

### Step 2: Configure the Script

Open the script and update the `filepath` variable to point to your System Verilog file. For example:

```python
filepath = r'C:\Users\mutth\study\Final Project\system_verilog_testbench_generator\file.sv'
```

### Step 3: Run the Script

Execute the script using Python:

```bash
python generate_testbench.py
```

The script will parse the System Verilog file, generate test vectors, monitor outputs, and create a testbench. The generated testbench will be saved in the same directory as the System Verilog file with the name `generated_testbench.sv`.

### Step 4: Run the Generated Testbench

Load the generated testbench in your simulation tool (e.g., QuestaSim) and run the simulation.

## File Structure

- `generate_testbench.py`: Main Python script to generate the testbench.
- `file.sv`: Example System Verilog file (replace with your own file).
- `generated_testbench.sv`: The generated testbench file.

## Script Breakdown

### `RESERVED_KEYWORDS`

List of System Verilog reserved keywords to avoid naming conflicts.

### `sanitize_signal_name(signal_name)`

Sanitizes the signal name to ensure it is not a reserved keyword. If the signal name is a reserved keyword, it appends `_sig` to the name.

### `parse_system_verilog(filepath)`

Parses a System Verilog file and returns a representation of the design. The design includes modules, signals, and parameters.

### `generate_test_vectors(signals)`

Generates test vectors for the design.

### `monitor_output(signals)`

Monitors the output of the design under test.

### `setup_simulation(modules, signals, test_vectors, monitor)`

Sets up the simulation environment.

### `save_testbench(output_dir, simulation_code)`

Saves the generated testbench to a file.

### `analyze_results()`

Analyzes the results of the simulation.

### `main()`

Main function to generate the testbench for the System Verilog design.

## Example

### System Verilog File (`file.sv`)

```verilog
module counter (
    input wire clk,
    input wire res_n,
    output reg [7:0] cnt_out
);

    // Internal signal for counting
    reg [7:0] count;

    // Synchronous counter
    always @(posedge clk or negedge res_n) begin
        if (!res_n) begin
            // Reset condition
            count <= 8'b0;
        end else begin
            // Count up condition
            count <= count + 1;
        end
    end

    // Assign output
    assign cnt_out = count;

endmodule
```

### Generated Testbench (`generated_testbench.sv`)

```systemverilog
`timescale 1ns / 1ps

module counter_tb;

  // Declare variables for the inputs and outputs of the DUT (Device Under Test)
  reg clk;
  reg res_n;
  wire [7:0] cnt_out;

  // Instantiate the DUT
  counter uut (
    .clk(clk),
    .res_n(res_n),
    .cnt_out(cnt_out)
  );

  // Test vectors
  initial begin
    // Initialize inputs and apply test vectors
    clk = 0;
    res_n = 0;
    // Apply test vectors
    #10;
    res_n = 1;
    #10;
    forever #5 clk = ~clk;
  end

  // Monitor changes
  initial begin
    $monitor("At time %0t: clk = %b, res_n = %b, cnt_out = %b", $time, clk, res_n, cnt_out);
  end

  // End simulation after a set period
  initial begin
    #200 $finish;
  end

endmodule
```

## Contributing

Feel free to submit issues or pull requests if you have any suggestions or improvements.

## Author
Rutuja Muttha
