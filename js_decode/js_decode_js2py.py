import re
import json
from js2py import eval_js

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
    # Use js2py to run the script
    eval_js(modified_js_code)
except Exception as error:
    print(f"Script execution failed: {error}")

# Define a custom serializer to handle circular references
def custom_serializer(obj):
    if isinstance(obj, JsObject):
        return obj.to_dict()

    if isinstance(obj, dict):
        return {key: custom_serializer(value) for key, value in obj.items()}

    if isinstance(obj, list):
        return [custom_serializer(item) for item in obj]

    return obj

class JsObject:
    def __init__(self, js_obj):
        self.js_obj = js_obj

    def to_dict(self):
        return {key: custom_serializer(value) for key, value in self.js_obj.items()}

# Extract properties from the global context
try:
    window_obj = eval_js("window")
    extracted_data = custom_serializer(window_obj)
except Exception as error:
    print(f"Error extracting data: {error}")
    extracted_data = None

# Print the modified JSON
if extracted_data is not None:
    print(json.dumps(extracted_data, indent=2))
