import re
import ast
from js_decode.animals import animals


def decode_hex_string(js_script):
    hex_string = re.search(r"var b=\"(.*?)\"", js_script).group(1)
    decoded_string = ''
    for i in range(0, len(hex_string), 2):
        decoded_string += chr(int(hex_string[i:i+2], 16))
    return decoded_string


def simplify_js_variables(js_script):
    variable_names, function_names = extract_variables_and_functions(js_script)
    new_variables, new_functions = new_words_with_prefix(variable_names, 'var'), new_words_with_prefix(function_names, 'func')
    decoded_with_variables = replace_words(js_script, variable_names, new_variables)
    decoded_with_functions = replace_words(decoded_with_variables, function_names, new_functions)
    return decoded_with_functions

def new_words_with_prefix(ordered_list, prefix):
    new_words = generate_animal_list(ordered_list)
    new_list = []
    for word in new_words:
        new_list.append(f'{prefix}_{word}')
    return new_list



def replace_words(long_string, words_to_replace, replacement_words):
    for word_to_replace, replacement_word in zip(words_to_replace, replacement_words):
        long_string = long_string.replace(word_to_replace, str(replacement_word))
    return long_string


def generate_animal_list(input_list):
    return [f'{animals[i + 1]}' for i in range(len(input_list))]



def complete_decode(js_script):
    b_value = re.search(r"var b=\"(.*?)\"", js_script).group(1)
    new_string = ''
    #string_list = hex_to_ascii(b_value)
    #string_value = ''.join(string_list)
    string_value = single_string_from_hex(b_value)
    string_split = string_value.split("'")
    for item in string_split:
        if '\\' in item:
            try:
                #temp = '"' + interpret_escaped_binary(item).decode('unicode_escape').decode('latin-1')
                temp = '"' + interpret_escaped_binary(item).decode('unicode_escape').decode('utf-8')
                new_string += temp
            except:
                new_string += '"' + interpret_escaped_binary(item)
        else:
            new_string += '"' + item
    return new_string.replace('"', "'")[1:]


def simplify_variable_names(js_code):
    # Extract variable names
    variable_pattern = r'\bvar\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\b'
    variable_names = re.findall(variable_pattern, js_code)
    # Create a list of simplified names
    simplified_names = [f'var_{i + 1}' for i in range(len(variable_names))]
    # Replace variable names with simplified names in the JavaScript code
    for old_name, new_name in zip(variable_names, simplified_names):
        js_code = js_code.replace(old_name, new_name)
    return simplified_names, js_code



def extract_variables_and_functions(js_code):
    # Regular expressions for variable and function names
    variable_pattern = r'\bvar\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\b'
    function_pattern = r'\bfunction\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\b'
    # Find all variable and function names using regular expressions
    variable_names = re.findall(variable_pattern, js_code)
    function_names = re.findall(function_pattern, js_code)
    return variable_names, function_names



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



#decoded = complete_decode(b_value)
#lists = extract_lists_from_string(decoded)