import json


def read_input_file(file):
    data = []
    with open(file, "r") as f:
        for line in f:
            data.append(json.loads(line))

    return data
