import json
import os
import re
import hcl


def extract_code_blocks_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        code_blocks = re.findall(r'```hcl\n(.*?)```', content, re.DOTALL)
        parsed_blocks = []
        for code_block in code_blocks:
            parsed_block = re.sub(r'\.\.\.', r'// ...', code_block)
            parsed_blocks.append(parsed_block)
        return parsed_blocks


def extract_code_blocks_from_directory(directory_path):
    result = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                file_path = os.path.join(root, file)
                code_blocks = extract_code_blocks_from_file(file_path)
                result.extend(code_blocks)
    return result


def parse_terraform(arr):
    hcl_arr = []
    for i, el in enumerate(arr):
        try:
            hcl_arr.append(hcl.loads(el))
        except Exception as e:
            print(f"Error parsing HCL: {e}")
            print(f"El: {i}")
            print(el)
    return hcl_arr


def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, elem in enumerate(v):
                if isinstance(elem, dict):
                    items.extend(flatten_dict(elem, f"{new_key}[{i}]", sep=sep).items())
                else:
                    items.append((f"{new_key}[{i}]", elem))
        else:
            items.append((new_key, v))
    return dict(items)


def main():
    # Step 1
    code_blocks = extract_code_blocks_from_directory(r"./docs/aws")

    # Step 2
    hcl_arr = parse_terraform(code_blocks)

    # Step 3
    flattened_arr = [flatten_dict(item) for item in hcl_arr]

    result = {}
    for d in flattened_arr:
        for key, value in d.items():
            if key in result:
                if value not in result[key]:
                    result[key].append(value)
            else:
                result[key] = [value]

    # Write result to file
    with open("./results/aws.json", 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
