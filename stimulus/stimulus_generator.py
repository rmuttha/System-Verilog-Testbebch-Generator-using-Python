def generate_stimulus(design):
    """
    Generates stimulus for the design.
    """
    stimulus = []
    for signal in design['signals']:
        # Generate random or predetermined test vectors
        stimulus.append(f"{signal[1]} = 'b0;")
        stimulus.append(f"{signal[1]} = 'b1;")
    return stimulus
