import os
import smtplib
from datetime import timedelta
from flask import Flask, render_template, flash, request, session, redirect, url_for
from wtforms import Form, IntegerField, TextField, TextAreaField, validators, StringField, SubmitField
from markupsafe import escape

application = Flask(__name__)
application.config.from_object(__name__)
application.config['SECRET_KEY'] = os.urandom(24)
application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
role_list = ['CW','CO','SH','PL','TW','ME','RI','FI']
result = {}

port = 587
smtp_server = 'smtp-relay.sendinblue.com'
username = 'jcyeh@familyfirstnetwork.org'
password = '3fJCwD8sV1KAI2aW'

from_add = 'jcyeh@familyfirstnetwork.org'
to_add = 'jcyeh@larc.ee.nthu.edu.tw'

sender = from_add
receivers = [to_add]

message = f"""\
Subject: TEST MAIL 4
To: {to_add}
From: {from_add}

This is test mail 4!"""

def Letter_Decode (i):
    return ord(i)-65

mapping_list = [
['G','D','F','C','A','H','B','E'],
['A','B','E','G','C','D','F','H'],
['H','A','C','D','F','G','E','B'],
['D','H','B','E','G','C','A','F'],
['B','F','D','H','E','A','C','G'],
['F','C','G','A','H','E','B','D'],
['E','G','A','F','D','B','H','C']]

class BelbinTeamRolesForm(Form):
    Answer=[]
    for i in range(1, 9):
        Answer.append(IntegerField("A{0}".format(i), validators=[validators.number_range(min=0, max=10)]))

class RegForm(Form):
    name = TextField('Name:', validators=[validators.input_required()])
    email = TextField('Email:', validators=[validators.input_required(), validators.Email(), validators.Length(min=6, max=35)])

@application.route("/", methods=['GET', 'POST'])
def index():
    global result
    form = RegForm(request.form)
    #print(form.errors)
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']

    if form.validate():
        # Save the comment here.
        session['username'] = name
        session['email'] = email
        result[email] = {}
        result[email]['username'] = name
        return redirect(url_for('Form_Q', qID=1))
    else:
        flash('Error: 請填寫正確的 email address, 才能收到測驗結果喲!')

    return render_template('regform.html', form=form)

@application.route('/Form_Q<int:qID>', methods=['GET', 'POST'])
def Form_Q(qID):
    global result
    form = BelbinTeamRolesForm(request.form)
    email = session.get('email')
    QID = escape(qID)
    Answer=[]
    #print(form.errors)
    if request.method == 'POST':
        for i in range(1, 9):
            value = request.form["A{0}".format(i)]
            Answer.append(int(value) if value else 0)

    if form.validate() and sum(Answer) == 10:
        # Save the comment here.
        result[email]["Q" + str(QID)] = Answer
        if int(QID) == 7:
            return redirect(url_for('Done'))
        else:
            return redirect(url_for('Form_Q', qID=int(QID) + 1))
    else:
        flash('Error: 總分必需等於 10 ')

    return render_template("Q" + str(QID) + ".html", form=form)

@application.route('/Done')
def Done():
    global result
    email = session.get('email')
    i = 0
    for role in role_list:
        result[email][role] = 0
    for mapping in mapping_list:
        i = i + 1
        for idx in range(len(role_list)):
            result[email][role_list[idx]] = result[email][role_list[idx]] + result[email]["Q" + str(i)][Letter_Decode(mapping[idx])]
    return '<h2>太棒了, {0}!  你已完成測試!  測試結果已送至你的 Email<{1}> 囉!</h2>'.format(result[email]['username'], email)
    # result[email]['CW'],
    #    result[email]['CO'],result[email]['SH'],result[email]['PL'],result[email]['TW'],result[email]['ME'],result[email]['RI'],result[email]['FI'])
    #print('Finished the test!')

if __name__ == "__main__":
    application.run()
