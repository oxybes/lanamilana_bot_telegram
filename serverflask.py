import os
import json
from flask import Flask, request
from database.function import DataBaseFunc

app = Flask(__name__)

@app.route('/', methods=["POST"])
def index():
    data = request.json
    phone = data['phone']
    mail = data['mail']
    course_id = data['course_id']
    is_added = DataBaseFunc.add_contact(phone, mail, course_id)
    return str(is_added)

@app.route('/delete', methods=["POST"])
def delete():
    data = request.json
    is_delete = DataBaseFunc.delete_contact(data['phone'], data['mail'])
    return str(is_delete)

@app.route('/testhook', methods=["POST"])
def testhook():
    data = request.json
    with open("//root//testhook.json", 'w', encoding='utf8') as file:
        json.dump(data, file)
    return "ok"

@app.route('/test')
def test():
    return "Hello world"

if __name__ == "__main__":
    if (os.name == "nt"):
        app.run(debug=True)
    else:
        app.run(host="193.187.175.22", port="8080")