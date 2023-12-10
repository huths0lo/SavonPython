import re
import json
from py_mini_racer import py_mini_racer

# Read the JavaScript file
js_file_path = "javascript.js"  # Replace with your file path
with open(js_file_path, "r") as file:
    js_code = file.read()

# Function to hexify the code
def hexify(text):
    return text.encode("utf-8").hex()

# Hexify the variable 'b'
hexified_variable = hexify("STRING")
modified_js_code = re.sub(
    r"var\s+b\s*=\s*'STRING';", f"var b = '{hexified_variable}';", js_code
)

# Run the modified JavaScript code
try:
    # Use py_mini_racer to run the script
    racer = py_mini_racer.MiniRacer()
    racer.execute(modified_js_code)
except Exception as error:
    print(f"Script execution failed: {error}")

# Extract properties from the global context
try:
    window_obj = racer.execute("window")
    extracted_data = json.loads(window_obj.json_dump())
except Exception as error:
    print(f"Error extracting data: {error}")
    extracted_data = None

# Print the modified JSON
if extracted_data is not None:
    print(json.dumps(extracted_data, indent=2))
