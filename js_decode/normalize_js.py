import re
import ast

with open('js_script.js', 'r') as f:
    js_script = f.read()


b_value = re.search(r"var b=\"(.*?)\"", js_script).group(1)


def complete_decode(b_value):
    new_string = ''
    string_list = hex_to_ascii(b_value)
    string_value = ''.join(string_list)
    string_split = string_value.split("'")
    for item in string_split:
        if '\\' in item:
            try:
                temp = '"' + interpret_escaped_binary(item).decode('unicode_escape')
                new_string += temp
            except:
                new_string += '"' + interpret_escaped_binary(item)
        else:
            new_string += '"' + item
    return new_string



def complete_decode(b_value):
    new_string = ''
    string_list = hex_to_ascii(b_value)
    string_value = ''.join(string_list)
    string_split = string_value.split("'")
    for item in string_split:
        if '\\' in item:
            try:
                temp = '"' + interpret_escaped_binary(item).decode('unicode_escape')
                new_string += temp
            except:
                new_string += '"' + interpret_escaped_binary(item)
        else:
            new_string += '"' + item
    return new_string


def single_string_from_hex(b):
    string = ''
    for i in range(0, len(b), 2):
        hex_pair = b[i:i + 2]
        decimal_value = int(hex_pair, 16)
        string += (chr(decimal_value))
    return string

def hex_to_ascii(b):
    string_list = []
    for i in range(0, len(b), 2):
        hex_pair = b[i:i + 2]
        decimal_value = int(hex_pair, 16)
        string_list.append(chr(decimal_value))
    return string_list

def interpret_escaped_binary(binary_string):
    # Convert binary to ASCII by interpreting escaped binary
    binary_values = [value for value in binary_string.split('\\x') if value]
    try:
        ascii_characters = [chr(int(value, 16)) for value in binary_values]
        return ''.join(ascii_characters)
    except ValueError:
        return ''







def extract_lists_from_string(input_string):
    # Use a regular expression to find all lists in the input string
    list_pattern = r'\[.*?\]'
    lists_found = re.findall(list_pattern, input_string)
    # Convert the found strings to Python lists using ast.literal_eval
    extracted_lists = [ast.literal_eval(lst) for lst in lists_found]
    return extracted_lists



decoded = complete_decode(b_value)
#lists = extract_lists_from_string(decoded)