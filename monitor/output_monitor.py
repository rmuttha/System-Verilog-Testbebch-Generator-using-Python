def monitor_output(design):
    """
    Monitors the output of the design under test.
    """
    with open('output_monitor.sv', 'w') as file:
        file.write("// Output Monitor\n")
        for signal in design['signals']:
            if signal[0] == 'output':
                file.write(f"initial begin\n  $monitor(\"%b\", {signal[1]});\nend\n")
