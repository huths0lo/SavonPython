const fs = require('fs');
const { JSDOM } = require('jsdom');

// Read the JavaScript file
const jsFilePath = process.argv[2];

if (!jsFilePath) {
  console.error('Usage: node wrapper.js <javascript_file>');
  process.exit(1);
}

const jsCode = fs.readFileSync(jsFilePath, 'utf8');

// Function to hexify the code
const hexify = (text) => {
  return Buffer.from(text, 'utf8').toString('hex');
};

// Hexify the variable 'b'
const hexifiedVariable = hexify('STRING');
const modifiedJsCode = jsCode.replace(/var\s+b\s*=\s*'STRING';/, `var b = '${hexifiedVariable}';`);

// Create a virtual DOM environment
const { window } = new JSDOM();

// Expose the window object globally
global.window = window;

// Run the modified JavaScript code
try {
  // Use the built-in vm module to run the script
  require('vm').runInThisContext(modifiedJsCode, { filename: jsFilePath });
} catch (error) {
  console.error(error.message);
}

// Output all variables set in the script
console.log(window);