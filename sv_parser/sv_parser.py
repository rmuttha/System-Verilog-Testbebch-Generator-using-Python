import re

def parse_system_verilog(filepath):
    """
    Parses a System Verilog file and returns a representation of the design.
    """
    design = {
        'modules': [],
        'signals': [],
        'parameters': []
    }

    with open(filepath, 'r') as file:
        content = file.read()

    # Simple regex-based parsing for modules, signals, and parameters
    modules = re.findall(r'\bmodule\s+(\w+)', content)
    signals = re.findall(r'\b(input|output|inout|wire|reg)\s+\w+\s+(\w+)', content)
    parameters = re.findall(r'\bparameter\s+\w+\s+(\w+)', content)

    design['modules'] = modules
    design['signals'] = signals
    design['parameters'] = parameters

    return design
