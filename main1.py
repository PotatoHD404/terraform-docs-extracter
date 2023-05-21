import json

import hcl


def parse_terraform_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        arr = json.load(f)
        hcl_arr = []
        for i, el in enumerate(arr):

            try:
                hcl_arr.append(hcl.loads(el))
            except Exception as e:
                print(f"Error parsing HCL: {e}")
                print(f"El: {i}")
                print(el)
                # return None
        return hcl_arr


def main():
    hcl_arr = parse_terraform_file('./results/aws/1.json')
    with open("./results/aws/2.json", 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(hcl_arr, indent=4))


if __name__ == "__main__":
    main()
