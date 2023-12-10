import re

b_value = re.search(r"var b=\"(.*?)\"", test).group(1)
b_split = b_value.split('39')
get_eval_js = re.search(r"eval(.*?)\}", test).group(1)


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

def decode_binary_strings(input_string):
    binary_strings = input_string.split("','")
    decoded_strings = [interpret_escaped_binary(binary) for binary in binary_strings]
    result = ''.join(decoded_strings)
    return result


def find_binary(string_split):
    new_string = "'"
    for item in string_split:
        check = interpret_escaped_binary(item)
        if check != '':
            new_string += check + "'"
        else:
            new_string += item + "'"
    return new_string

string_list = hex_to_ascii(b_value)
string_value = ''.join(string_list)
# Example usage:
string_split = string_value.split("'")



decoded_string = interpret_escaped_binary(string_value)

# Example usage:
input_string = "var _0x01c1=['\\x77\\x71\\x38\\x61\\x65\\x41\\x3d\\x3d','\\x77\\x71\\x4e\\x36\\x41\\x73\\x4b\\x6d\\x77\\x72\\x50\\x43\\x76\\x67\\x3d\\x3d','\\x77\\x35\\x48\\x44\\x6e\\x6c\\x6a\\x43\\x74\\x41\\x3d\\x3d'"
decoded_result = decode_binary_strings(input_string)

print("Original Input String:", input_string)
print("Decoded Result:", decoded_result)




def get_string(b_split):
    text_list = []
    for nibble in b_split:
        text_list.append(hex_to_ascii(nibble))
    return text_list

.decode('latin-1')


def hex_to_ascii(b):
    z = ""
    for i in range(0, len(b), 2):
        hex_pair = b[i:i + 2]
        decimal_value = int(hex_pair, 16)
        z += chr(decimal_value)
    return z


text_list = get_string(b_split)

js_string -


def hex_to_dec(b_value):
    all_decimals = []
    for i in range(0, len(b_value), 2):
        hex_pair = b_value[i:i + 2]
        decimal_value = int(hex_pair, 16)
        all_decimals.append(decimal_value)
    return all_decimals


all_decimals = hex_to_dec(b_value)


def process_decimals(decimals):
    result = ""
    temp_decimal_string = ""
    for decimal in decimals:
        if decimal == 39:
            # If the decimal is 39, interpret the ASCII from the temporary string and append to the result
            result += interpret_escaped_binary(temp_decimal_string)
            temp_decimal_string = ""  # Reset the temporary string
        else:
            temp_decimal_string += str(decimal) + " "  # Add the decimal to the temporary string
    # Append any remaining interpreted ASCII from the last temporary string
    result += interpret_escaped_binary(temp_decimal_string)
    return result


def interpret_escaped_binary(decimal_string):
    # Convert decimals to binary and interpret ASCII from escaped binary
    binary_values = decimal_string.split()
    ascii_characters = [chr(int(binary, 16)) for binary in binary_values]
    return ''.join(ascii_characters)


string_value = process_decimals(all_decimals)

v
118
a
97
r
114
32
_
95
0
48
x
120
0
48
1
49
c
99
1
49
= 61
[91
 ' 39
\ 92
x
120
7
55
7
55
\ 92
x
120
7
55
1
49
\ 92
x
120
3
51
8
56
\ 92
x
120
6
54
1
49
\ 92
x
120
6
54
5
53
\ 92
x
120
4
52
1
49
\ 92
x
120
3
51
d
100
\ 92
x
120
3
51
d
100
' 39
, 44
' 39
\ 92
x
120
7
55
7
55
\ 92
x
120
7
55
1
49
\ 92
x
120
4
52
e
101
\ 92
x
120
3
51
6
54
\ 92
x
120
4
52
1
49
\ 92
x
120
7
55
3
51
\ 92
x
120
4
52
b
98
\ 92
x
120
6
54
d
100
\ 92
x
120
7
55
7
55
\ 92
x
120
7
55
2
50
\ 92
x
120
5
53
0
48
\ 92
x
120
4
52
3
51
\ 92
x
120
7
55
6
54
\ 92
x
120
6
54
7
55
\ 92
x
120
3
51
d
100
\ 92
x
120
3
51
d
100
' 39
, 44
' 39
\ 92
x
120
7
55
7
55
\ 92
x
120
3
51
5
53
\ 92
x
120
4
52
8
56
\ 92
x
120
4
52
4
52
\ 92
x
120
6
54
e
101
\ 92
x
120
6
54
c
99
\ 92
x
120
6
54
a
97
\ 92
x
120
4
52
3
51
\ 92
x
120
7
55
4
52
\ 92
x
120
4
52
1
49
\ 92
x
120
3
51
d
100
\ 92
x
120
3
51
d
100
' 39
, 44
' 39
\ 92
x
120
7
55
7
55
\ 92
x
120
7
55
1
49
\ 92
x
120
7
55
6
54
\ 92
x
120
4
52
3
51
\ 92
x
120
7
55
5
53
\ 92
x
120
4
52
2
50
\ 92
x
120
5
53
5
53
\ 92
x
120
3
51
3
51
\ 92
x
120
7
55
7
55
\ 92
x
120
7
55
2
50
\ 92
x
120
6
54
e
101
\ 92
x
120
4
52
4
52
\ 92
x
120
6
54
d
100
\ 92
x
120
6
54
7
55
\ 92
x
120
3
51
5
53
\ 92
x
120
7
55
8
56
\ 92
x
120
4
52
5
53
\ 92
x
120
3
51
8
56
\ 92
x
120
4
52
f
102
\ 92
x
120
5
53
a
97
\ 92
x
120
4
52
b
98
\ 92
x
120
4
52
d
100
\ 92
x
120
4
52
f
102
\ 92
x
120
7
55
2
50
\ 92
x
120
4
52
3
51
\ 92
x
120
6
54
c
99
\ 92
x
120
5
53
0
48
\ 92
x
120
4
52
3
51
\ 92
x
120
6
54
c
99
\ 92
x
120
3
51
8
56
\ 92
x
120
4
52
b
98
\ 92
x
120
2
50
b
98
\ 92
x
120
7
55
7
55
\ 92
x
120
3
51
6
54
\ 92
x
120
5
53
5
53
\ 92
x
120
4
52
a
97
\ 92
x
120
5
53
a
97
\ 92
x
120
3
51
8
56
\ 92
x
120
4
52
b
98
\ 92
x
120
6
54
b
98
\ 92
x
120
7
55
7
55
\ 92
x
120
6
54
f
102
\ 92
x
120
5
53
a
97
\ 92
x
120
4
52
a
97
\ 92
x
120
7
55
7
55
\ 92
x
120
3
51
6
54
\ 92
x
120
5
53
0
48
\ 92
x
120
4
52
3
51
\ 92
x
120
7
55
5
53
\ 92
x
120
4
52
d
100
\ 92
x
120
4
52
b
98
\ 92
x
120
6
54
1
49
\ 92
x
120
7
55
7
55
\ 92
x
120
7
55
0
48
\ 92
x
120
4
52
a
97
\ 92
x
120
3
51
9
57
\ 92
x
120
4
52
3
51
\ 92
x
120
3
51
1
49
\ 92
x
120
6
54
4
52
\ 92
x
120
4
52
4
52
\ 92
x
120
7
55
7
55
\ 92
x
120
3
51
4
52
\ 92
x
120
3
51
7
55
\ 92
x
120
4
52
3
51
\ 92
x
120
6
54
9
57
\ 92
x
120
6
54
3
51
\ 92
x
120
4
52
b
98
\ 92
x
120
4
52
f
102
\ 92
x
120
4
52
5
53
\ 92
x
120
7
55
3
51
\ 92
x
120
4
52
f
102
\ 92
x
120
7
55
a
97
\ 92
x
120
7
55
7
55
\ 92
x
120
6
54
f
102
\ 92
x
120
7
55
6
54
\ 92
x
120
4
52
3
51
\ 92
x
120
6
54
8
56
\ 92
x
120
3
51
3
51
\ 92
x
120
6
54
4
52
\ 92
x
120
6
54
9
57
\ 92
x
120
7
55
7
55
\ 92
x
120
6
54
f
102
\ 92
x
120
6
54
3
51
\ 92
  >> >