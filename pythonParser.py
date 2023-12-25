import re

def extract_typedef_enum_with_comments(c_code):
    typedef_enum_pattern = re.compile(r'typedef\s+enum\s*{([^}]*)}\s*([^;]+);', re.DOTALL)
    typedef_enum_matches = typedef_enum_pattern.findall(c_code)

    typedef_enum_data = []
    for enum_body, enum_name in typedef_enum_matches:
        enum_values = re.findall(r'(\w+)\s*(?:=\s*([^,]+))?,?\s*(?:\/\*([^*]+)\*\/)?', enum_body)
        enum_info = {
            'name': enum_name.strip(),
            'values': [{'name': value[0].strip(), 'default_value': value[1], 'comment': value[2].strip() if value[2] else None} for value in enum_values]
        }
        typedef_enum_data.append(enum_info)

    return typedef_enum_data

# Example usage
c_code = """
typedef enum {
    ENUM_VALUE_1,   /**< Comment for ENUM_VALUE_1 */
    ENUM_VALUE_2 = 5,   /**< Comment for ENUM_VALUE_2 */
    ENUM_VALUE_3    /**< Comment for ENUM_VALUE_3 */
} MyEnum;

typedef enum {
    ANOTHER_VALUE_1 = 10,   /**< Comment for ANOTHER_VALUE_1 */
    ANOTHER_VALUE_2,   /**< Comment for ANOTHER_VALUE_2 */
    ANOTHER_VALUE_3 = 15   /**< Comment for ANOTHER_VALUE_3 */
} AnotherEnum;
"""

typedef_enum_data = extract_typedef_enum_with_comments(c_code)

# Print the extracted typedef enum data with comments
for enum_info in typedef_enum_data:
    print(f"Enum Name: {enum_info['name']}")
    print("Enum Values:")
    for value_info in enum_info['values']:
        print(f"  Name: {value_info['name']}")
        print(f"  Default Value: {value_info['default_value']}")
        print(f"  Comment: {value_info['comment']}")
    print()
