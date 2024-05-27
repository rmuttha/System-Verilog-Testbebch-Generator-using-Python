def generate_assertions(design):
    """
    Generates assertions for the design.
    """
    with open('assertions.sv', 'w') as file:
        file.write("// Assertions\n")
        for param in design['parameters']:
            file.write(f"assert ({param} == expected_value) else $fatal(\"{param} assertion failed\");\n")
