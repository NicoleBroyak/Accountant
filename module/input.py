def input_mode(ALLOWED_COMMANDS):
    mode = input("Please type mode:")
    while mode not in ALLOWED_COMMANDS:
        mode = input("Please type mode:")
    return mode