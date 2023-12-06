import re

def remove_comments(text):
    # Remove single-line comments
    text = re.sub(r'\/\/.*', '', text)

    # Remove multi-line comments
    text = re.sub(r'\/\*.*?\*\/', '', text, flags=re.DOTALL)

    return text

def parse_typedef_enum(text):
    enum_pattern = re.compile(r'typedef\s+enum\s*{([^}]*)}\s*([^;]+);')
    matches = enum_pattern.finditer(text)

    enums = []

    for match in matches:
        enum_body = match.group(1)
        enum_name = match.group(2).strip()
        
        enum_values = [item.strip() for item in enum_body.split(',')]
        
        enums.append({
            'name': enum_name,
            'values': enum_values
        })

    return enums

def main():
    input_file_path = 'header.h'
    output_file_path = 'output_file.h'

    with open(input_file_path, 'r') as file:
        file_content = file.read()

    # Remove comments
    cleaned_content = remove_comments(file_content)

    # Parse and extract typedef enums
    enums = parse_typedef_enum(cleaned_content)

    # Print or do something with the extracted enums
    for enum in enums:
        print(f"Enum Name: {enum['name']}")
        print(f"Enum Values: {enum['values']}")
        print()

    # Optionally, save the cleaned content to a new file
    with open(output_file_path, 'w') as output_file:
        output_file.write(cleaned_content)

if __name__ == "__main__":
    main()
