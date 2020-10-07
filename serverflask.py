import os
from flask import Flask, request
from database.function import DataBaseFunc

app = Flask(__name__)

@app.route('/', methods=["POST"])
def index():
    data = request.json
    is_added = DataBaseFunc.add_contact(data['phone'], data['mail'])
    return str(is_added)

@app.route('/delete', methods=["POST"])
def delete():
    data = request.json
    is_delete = DataBaseFunc.delete_contact(data['phone'], data['mail'])
    return str(is_delete)

if __name__ == "__main__":
    if (os.name == "nt"):
        app.run(debug=True)
    else:
        app.run("193.187.175.22", host="8080")