import json
import os
import re


def extract_code_blocks_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # Use regular expressions to find HCL code blocks
        code_blocks = re.findall(r'```hcl\n(.*?)```', content, re.DOTALL)
        parsed_blocks = []
        for code_block in code_blocks:
            # Add "// " before any "..."
            parsed_block = re.sub(r'\.\.\.', r'// ...', code_block)
            parsed_blocks.append(parsed_block)
        return parsed_blocks


def extract_code_blocks_from_directory(directory_path, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        result = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.md') or file.endswith('.markdown'):
                    file_path = os.path.join(root, file)
                    code_blocks = extract_code_blocks_from_file(file_path)
                    result.extend(code_blocks)
                    # for code_block in code_blocks:
                    #     output_file.write(code_block + '\n')
        output_file.write(json.dumps(result, indent=4))


def main():
    extract_code_blocks_from_directory(r"./docs/yandex",
                                       "./results/yandex/1.json")


if __name__ == "__main__":
    main()
