import re

def parse_enum(c_code):
    enum_dict = {}

    # Regular expression to match typedef enum
    enum_pattern = re.compile(r'typedef\s+enum\s*{([^}]*)}\s*([^;]+);', re.DOTALL)

    # Regular expression to match enum values and comments
    enum_values_pattern = re.compile(r'(\w+)\s*(?:=\s*([^,]+))?,?\s*(?:\/\*([^*]+)\*\/)?')

    # Find typedef enum
    enum_match = enum_pattern.search(c_code)

    if enum_match:
        enum_body = enum_match.group(1)
        enum_name = enum_match.group(2)

        # Find enum values and comments
        enum_values_matches = enum_values_pattern.findall(enum_body)

        # Store in dictionary
        enum_values = []
        for value, default_value, comment in enum_values_matches:
            enum_values.append({
                'name': value,
                'default_value': default_value if default_value else None,
                'comment': comment.strip() if comment else None
            })

        enum_dict[enum_name] = enum_values

    return enum_dict

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

enum_dict = parse_enum(c_code)

for enum_name, enum_values in enum_dict.items():
    print(f"Enum Name: {enum_name}")
    print("Enum Values:")
    for enum_value in enum_values:
        print(f"  Name: {enum_value['name']}")
        print(f"  Default Value: {enum_value['default_value']}")
        print(f"  Comment: {enum_value['comment']}")
        print()
