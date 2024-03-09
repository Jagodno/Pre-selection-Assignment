def get_descriptions(fname):
    descriptions = {}
    with open(fname , 'r') as file:
        for line in file:
            argname, argvalue = line.split(maxsplit=1)
            descriptions[argname] = argvalue.strip()
    return descriptions