from flask import Flask
from flask import request
from flask import jsonify
import json
from source import entryPoint

app = Flask(__name__)

@app.route('/')
def default():
    return "hello"

@app.route('/hook',methods=['POST'])
def github_hook():
    print("github payload received")
    requestData = request.json
    return entryPoint.main(requestData)

@app.errorhandler(500)
def internal_error(error):
    print(error)
    return "500 error",500

@app.errorhandler(404)
def not_found(error):
    prit(error)
    return "404 error",404

def load_config():
    with open('config.json') as config_file:    
        return json.load(config_file)

if __name__ == '__main__':
    config = load_config()
    app.run(host=config.get('host', 'localhost'), port=config.get('port', 8000))
