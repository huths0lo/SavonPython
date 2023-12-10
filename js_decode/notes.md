I have used open ai to create a wrapper.  This wrapper will take in another js file as a variable with:

node javascript_decompile_wrapper.js js_script_to_decode.js

It takes the following actions:

1) Locates the b variable.
2) Dehexifies the b variable.
3) Creates a virtual js dom.
4) Instatiates the needed variables.
5) Executes the dehexified js within the js dom.
6) Captures the instructions into a json.
7) Prints json to console.

Ideally I'd like to create a python script that can do the same thing.  But since this requires the js dom, that may not be possible (at least not without selenium).

For now, this should give me what I desperately needed.  To use it, you must have node.js installed, along with the jsdom module.

npm install jsdom

npm install fs jsdom circular-jsonc