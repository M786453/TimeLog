from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

bg_colors = [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)'
            ]
borders = [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)'
            ]

def create_task_table():
    conn = sqlite3.connect('taskHistory.db')
    conn.execute('CREATE TABLE IF NOT EXISTS Task_History(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT , duration REAL, date DATE)')
    conn.commit()
    conn.close()
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/history')
def history():
    # return render_template('history.html')
    return redirect(url_for('daily_history'))

@app.route('/insert', methods = ['POST', 'GET'])
def insert_task():

    if 'task_name' in request.args:
        task_name = request.args.get('task_name')
        return render_template('log.html', task_name = task_name)
    
    return render_template('task.html')

   
@app.route('/task_done')
def task_done():
    if 'name' in request.args and 'duration' in request.args:
        conn = sqlite3.connect('taskHistory.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO Task_History (name, duration, date) values (?,?,?)' , (request.args['name'] , request.args['duration'], datetime.now().date()) )
        conn.commit()
        conn.close()
    return "task_done"


@app.route('/daily')
def daily_history():
    
    tasks = ["Freelancing", "Amal", "Household", "Others", "Naughty", "America","Asia","Pakistan", "India","China", "Afghanistan","Iran"]
    
    time_history = [12, 19, 3, 5, 2,1,20,6,11,30,4,2]
    
    return render_template('history.html', status = 'Daily', tasks=tasks, time_history=time_history, bg_colors=bg_colors, borders=borders)

@app.route('/monthly')
def monthly_history():

    tasks = ["Freelancing", "Amal", "Household", "Others"]
    
    time_history = [12, 19, 3, 5, 2]

    return render_template('history.html', status = 'Monthly', tasks=tasks, time_history=time_history, bg_colors=bg_colors, borders=borders)

@app.route('/yearly')
def yearly_history():
    
    tasks = ["Freelancing", "Amal", "Household", "Others"]
    
    time_history = [12, 19, 3, 5, 2]
    
    return render_template('history.html', status = 'Yearly', tasks=tasks, time_history=time_history, bg_colors=bg_colors, borders=borders)



if __name__ == "__main__":
    create_task_table()
    app.run(debug=True)
