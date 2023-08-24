import json


def read_input_file(file):
    data = []
    with open(file, "r") as f:
        for line in f:
            data.append(json.loads(line))

    return data


def read_output_file(file):
    return json.loads(open(file, "r").read())
