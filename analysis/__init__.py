import re
import sys

def extract_module_info(sv_code):
    module_info = {}
    module_name_pattern = r"module\s+(\w+)"
    ports_pattern = r"\((.*?)\);"
    
    module_name_match = re.search(module_name_pattern, sv_code)
    ports_match = re.search(ports_pattern, sv_code, re.DOTALL)
    
    if module_name_match and ports_match:
        module_info['name'] = module_name_match.group(1)
        ports = ports_match.group(1)
        # Remove comments from ports declaration
        ports = re.sub(r'\/\/.*?\n', '', ports)
        ports = ports.replace("\n", "")
        ports = ports.replace(" ", "")
        ports = ports.split(",")
        
        module_info['ports'] = []
        for port in ports:
            port_parts = port.split(":")
            if len(port_parts) == 2:
                port_info = port_parts[1].split()
                direction = port_parts[0]
                if len(port_info) == 2:
                    module_info['ports'].append((direction, port_info[0], port_info[1]))
                elif len(port_info) == 1:
                    module_info['ports'].append((direction, "logic", port_info[0]))
    return module_info

def analyze_sv_file(input_file):
    with open(input_file, 'r') as file:
        sv_code = file.read()
    
    module_info = extract_module_info(sv_code)
    
    if not module_info:
        print("Error: Could not extract module information from the input file.")
        sys.exit(1)
    
    print(f"The SystemVerilog code is for module: {module_info['name']}")

def main():
    print("Please enter the SystemVerilog file:")
    input_file = input()
    
    analyze_sv_file(input_file)

if __name__ == "__main__":
    main()
