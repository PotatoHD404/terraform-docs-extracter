import json


def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):   # check if value is a list
            for i, elem in enumerate(v):  # for each element in the list
                if isinstance(elem, dict):  # if element is a dictionary
                    items.extend(flatten_dict(elem, f"{new_key}[{i}]", sep=sep).items())
                else:
                    items.append((f"{new_key}[{i}]", elem))  # if not, just append the element with its index
        else:
            items.append((new_key, v))
    return dict(items)


def main():
    with open("./results/yandex/2.json", 'r', encoding='utf-8') as f:
        arr = json.load(f)

    flattened_arr = [flatten_dict(item) for item in arr]

    result = {}
    for d in flattened_arr:
        for key, value in d.items():
            if key in result:  # if key is in the result, append the value if not already present
                if value not in result[key]:
                    result[key].append(value)
            else:  # if key is not in the result, start a new list
                result[key] = [value]

    with open("./results/yandex/3.json", 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()