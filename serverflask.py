import os
import json
import re
import datetime
from flask import Flask, request, render_template
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


@app.route('/addcontact', methods=["GET", "POST"])
def addcontact():
    email ='' 
    phone ='' 
    id_course = ''
    message = 'id_course. 1 - Базовый, 2 - Всё, что нужно, 3 - индивидуальный. Для нового потока 12, 22, 32'
    if request.method == 'POST':
        email = request.form.get('email')  # запрос к данным формы
        phone = request.form.get('phone')
        id_course= request.form.get('id_course')
        if (email != '' and phone != '' and id_course != ''):
            phone = "".join(ch for ch in phone if  ch.isdigit())
            if (phone[0] == '8'):
                phone = '7' + phone[1:]
            email = email.lower()
            is_added = DataBaseFunc.add_contact(phone, email, id_course)
            if (is_added):
                message += "\n Добавлен"
            else:
                message += "\n Не добавлен (Возможно такой контакт уже есть"
    
    return render_template('addcontact.html', message=message)


def get_day(user):
    day = 0
    subs = DataBaseFunc.get_current_subscribe(user)
    if ((user.is_have_subscription) and (subs!= None)):
        day = (subs.data_end - datetime.datetime.now()).days
    return day

@app.route('/table')
def table():
    users = DataBaseFunc.get_users_for_table()
    return render_template('table.html', users=users, get_day=get_day)


@app.route('/delete', methods=["POST"])
def delete():
    data = request.json
    is_delete = DataBaseFunc.delete_contact(data['phone'], data['mail'])
    return str(is_delete)

@app.route('/testhook', methods=["POST"])
def testhook():
    form = request.form
    print(form)
    if form['test'] == 'test':
        return 'ok'
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
    return 'ok'


@app.route('/test')
def test():
    return "Hello world"

if __name__ == "__main__":
    if (os.name == "nt"):
        app.run(debug=True)
    else:
        app.run(host="193.187.174.95", port="8080")
