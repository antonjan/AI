from flask import Flask, render_template, request ,request, url_for
import subprocess
from functools import wraps
import csv

app = Flask(__name__)
# Define a username and password for access control
USERNAME = 'anton'
PASSWORD = 'llama2'
f = open('llama2.log', 'w')
# Function to check if the user is authenticated
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

# Function to require authentication for certain routes
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return 'Unauthorized', 401
        return f(*args, **kwargs)
    return decorated

# Define the path to your Llama2 AI CLI tool
llama2_cli_path = "/home/anton/llama.cpp/models/llama2-q8.gguf"

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    writer = csv.writer(f)
    user_key = ""
    user_input = request.form['user_input']
    user_key = request.form['user_key']
    if user_key == "5431": 
       print("user input",user_input)
       
       # Run the Llama2 AI CLI tool and capture the output
       #llama2_command = "/home/anton/llama2/llama.cpp/build/bin/main -m /home/anton/llama.cpp/models/llama2-q8.gguf -ngl 99 --color"
       command = f"/home/anton/llama2/llama.cpp/build/bin/main -m {llama2_cli_path} -ngl 99 --color -p '{user_input}' 2> null"
       #command = f"/home/anton/llama2/llama.cpp/build/bin/main -m {llama2_cli_path} -ngl 99 --color -p '{user_input}'" 
       #command = f'{llama2_command} -p "{user_input}"'
       print(command)
       #result = subprocess.getoutput(command) #["ls", "-l", "/dev/null"
       #result = subprocess.run(command, capture_output=True)
       result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

       #result = subprocess.run(command)
       #if result.stderr :
       #   print(".")

       result2 =  result.replace("\n", "<br>")
       print("results2",result)
       logdata = [user_input,result]
       writer.writerow(logdata) 
        
       return result2
    else:
       result = "There is no key supplyed with prompt, try again with corect key"
       return result
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

