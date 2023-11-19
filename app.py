from flask import Flask, render_template, request, redirect, url_for, session,flash
from datetime import datetime
import sqlite3
from dashboard import fetch_data, create_bar_chart, create_line_chart, create_pie_chart, create_heart_rate_scatter_plot
import pickle


app = Flask(__name__)
app.config['DATABASE'] = 'Cal.db'
app.secret_key = 'RandomKey@123'

model=pickle.load(open('ML\model.sav','rb'))

@app.route('/',methods=("GET","POST"))
def main():
    if request.method=="POST":
        pred = model.predict([[int(request.form['gender']),float(request.form['age']),float(request.form['height']),float(request.form['duration']),float(request.form['heart_rate']),float(request.form['temperature'])]])
        pred = round(float(pred),3)
        return render_template('index.html',calories = pred)
        
    return render_template('index.html')

@app.route('/login',methods=("GET","POST"))
def login():
    if request.method=="POST":
        login_id = request.form.get('uid')
        passwd = request.form['password']
        log_conn = sqlite3.connect(app.config['DATABASE'])
        curr=log_conn.cursor()
        curr.execute('SELECT name,age,height,gender FROM users WHERE uid = ? AND password = ?', (login_id,passwd))
        result = curr.fetchone()
        log_conn.close()
        if result != None:
            session['uid'] = request.form['uid']
            session['name'] = result[0]
            session['age'] = result[1]
            session['height'] = result[2]
            session['gender'] = result[3]
            return redirect(url_for('home'))
        else:
            flash("Wrong Id or Password", 'error')  # Flash an error message
            return render_template('login.html')

    return render_template('login.html')

@app.route('/register',methods=["POST"])
def register():
    uid=request.form['uid']
    passwd = request.form['password']
    name = request.form['name']
    age = request.form['age']
    height = request.form['height']
    gender = request.form['gender']
    reg_conn = sqlite3.connect(app.config['DATABASE'])
    reg_curr=reg_conn.cursor()
    reg_curr.execute('SELECT uid FROM users WHERE uid = ?', (uid,))
    result = reg_curr.fetchone()
    if result:
        reg_conn.close()
        flash("User already exists", 'error')  # Flash an error message
        return render_template('login.html')
    else:
        reg_curr.execute('insert into users values(?,?,?,?,?,?)',(uid,passwd,name,age,height,gender))
        reg_conn.commit()
        reg_conn.close()
        session['uid'] = request.form['uid']
        session['name'] = request.form['name']
        session['age'] = request.form['age']
        session['height'] = request.form['height']
        session['gender'] = request.form['gender']
        return redirect(url_for('home'))
        
@app.route('/home',methods=("GET","POST"))
def home():
    if request.method=="POST":
        pred = model.predict([[int(request.form['gender']),float(request.form['age']),float(request.form['height']),float(request.form['duration']),float(request.form['heart_rate']),float(request.form['temperature'])]])
        pred = round(float(pred),3)
        session['calories'] = pred
        ex_conn = sqlite3.connect(app.config['DATABASE'])
        ex_curr=ex_conn.cursor()
        ex_curr.execute('insert into exercise(e_name,uid,duration,date,bpm,temperature,calories) values(?,?,?,?,?,?,?)',
                             (request.form['e_name'],
                              session['uid'],
                              float(request.form['duration']),
                              datetime.today().date(),
                              float(request.form['heart_rate']),
                              float(request.form['temperature']),
                              pred))
        ex_conn.commit()
        ex_conn.close()
        return render_template('home.html',calories = pred)
        

    return render_template('home.html',name = session['name'], age = session['age'], height = session['height'], gender = 0 if session['gender']=='Male' else 1)

@app.route('/dashboard',methods=("GET","POST"))
def dashboard():
    user_name = session.get('name')
    uid = session.get('uid')
    if user_name:
        exercise_data, time_data, calories_data, heart_data = fetch_data(uid)

        bar_chart = create_bar_chart(exercise_data)
        line_chart = create_line_chart(time_data)
        pie_chart = create_pie_chart(calories_data, title='Exercise Distribution and Calories Burned')
        scatter_plot = create_heart_rate_scatter_plot(heart_data)


        return render_template('dashboard.html',
                               username=user_name,
                               bar_chart=bar_chart,
                               line_chart=line_chart,
                               pie_chart=pie_chart,
                               scatter_plot=scatter_plot
                            )


if __name__ == '__main__':
    app.run(debug=True)