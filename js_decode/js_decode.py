# This script takes in the contents of a variable (the variable is the raw text of a javascript.js), and writes it to a temporary file.
# It then calls node.js as a sub process, which in turn generates a json output.  We then hand back the json to the calling function.



import json
import subprocess
from datetime import datetime
import os

current_directory = os.getcwd()
wrapper_script = current_directory + '/js_decode/decompile_wrapper.js'

def generate_json_from_js(js_code):
    current_timestamp = datetime.now()
    timestamp_string = current_timestamp.strftime("%Y-%m-%d-%H:%M:%S")
    temp_file = f'{current_directory}/js_code{timestamp_string}.js'
    with open(temp_file, 'w') as f:
        f.write(js_code)
    json_vars = call_js_wrapper(temp_file)
    os.remove(temp_file)
    return json_vars


def call_js_wrapper(js_file_path):
    try:
        # Run the wrapper.js script using subprocess
        result = subprocess.run(['node', wrapper_script, js_file_path], capture_output=True, text=True, check=True)
        # Extract the standard output
        js_output = result.stdout
        # Parse the JavaScript output as JSON
        parsed_output = json.loads(js_output)
        return parsed_output
    except subprocess.CalledProcessError as e:
        print("Error calling wrapper.js:", e)
        return None