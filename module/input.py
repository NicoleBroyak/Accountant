inputlist = []

def input_list():
    input = inputlist[-1]
    inputlist.pop()
    return input

def input_mode(ALLOWED_COMMANDS):
    mode = input_list()
    while mode not in ALLOWED_COMMANDS:
        mode = input_list()
    return mode