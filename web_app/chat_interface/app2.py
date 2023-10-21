import subprocess
import re
from flask import Flask, request, jsonify

app = Flask(__name)

# Define the Llama2 command you provided
llama2_command = "./main -m /home/anton/llama.cpp/models/llama2-q8.gguf -ngl 99 --color"

# Route to handle the chat interface
@app.route('/chat', methods=['POST'])
def chat_with_llama2():
    # Get the user's message from the request
    user_message = request.json['message']
    
    # Construct the full command by appending the user's message to the Llama2 command
    full_command = f'{llama2_command} -p "{user_message}"'

    try:
        # Run the Llama2 command and capture the output
        output = subprocess.check_output(full_command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        
        # Remove any error messages from the output
        cleaned_output = re.sub(r'Error:.*', '', output)
        
        return jsonify({'response': cleaned_output})
    except subprocess.CalledProcessError as e:
        return jsonify({'response': f'An error occurred: {e.output}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

