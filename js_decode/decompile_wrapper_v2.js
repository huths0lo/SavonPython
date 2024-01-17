const fs = require('fs');
const { JSDOM } = require('jsdom');
const CircularJSON = require('circular-json');

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

// Create a virtual DOM environment with a permissive localStorage
const { window } = new JSDOM(``, { url: 'http://example.com', runScripts: 'outside-only' });

// Expose the window object globally
global.window = window;

// Run the modified JavaScript code
try {
  // Use the built-in vm module to run the script
  require('vm').runInThisContext(modifiedJsCode, { filename: jsFilePath });
} catch (error) {
  console.error(error.message);
}

// Extract relevant information and store in a JSON object
const extractedData = {
  url: window.location ? window.location.href : null,
  headers: window.document ? window.document.head.innerHTML : null,
  variables: CircularJSON.stringify(window, (key, value) => {
    // Exclude circular references and certain properties
    if (key === '_localStorage') return undefined;
    if (value && typeof value === 'object' && value.nodeType) return `[${value.nodeName}]`; // Check for a DOM node
    return value;
  }, 2),
};

// Output the JSON object
console.log(JSON.stringify(extractedData, null, 2));