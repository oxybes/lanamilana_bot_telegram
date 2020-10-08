import os
import json
import re

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
    form = request.form
    phone = "".join(ch for ch in form['Phone'] if  ch.isdigit())
    mail = form['Email']
    payment = form['payment']
    data = json.loads(payment)
    product = data['products'][-1]
    pattern = r'Тариф:(.*)'
    result = re.search(pattern, product).group(0)[:-3]
    if (result == "Тариф: Базовый тест"):
        id_tariff = 1
    elif (result == "Тариф: Всё, что нужно тест"):
        id_tariff = 2
    else:
        id_tariff = 3
    DataBaseFunc.add_contact(phone, mail, id_tariff)


@app.route('/test')
def test():
    return "Hello world"

if __name__ == "__main__":
    if (os.name == "nt"):
        app.run(debug=True)
    else:
        app.run(host="193.187.175.22", port="8080")