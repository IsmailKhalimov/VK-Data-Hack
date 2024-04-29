from Tags import tags
from flask import request
from flask import Flask, jsonify, abort
import json
import ast

app = Flask(name)


@app.route('/', methods=['GET', 'POST'])
def index():
    data = request.args.get('path')
    return jsonify(ast.literal_eval(tags(data)[1:-1]))

if name == 'main':
    app.run(debug=True)