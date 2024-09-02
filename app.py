from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)

CORS(app) # Enable cors for all routes

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

def get_task_history(mode):

    conn = sqlite3.connect('taskHistory.db')

    conn.row_factory = sqlite3.Row
    
    cur = conn.cursor()

    if mode == 'Daily':

        current_date = datetime.now().date()

        cur.execute("SELECT name, duration FROM Task_History WHERE date = ?", (current_date, ))
        
    
    elif mode == "Monthly":

        current_year_month = datetime.now().strftime('%Y-%m')

        cur.execute("SELECT name, duration FROM Task_History WHERE date LIKE ?", (f'{current_year_month}%',))

    elif mode == "Yearly":

        current_year = datetime.now().date().year

        cur.execute("SELECT name, duration FROM Task_History WHERE date LIKE ?", (f'{current_year}%',))

    # Data segregation

    tasks_data = cur.fetchall()

    tasks = []

    time_history = []

    for row in tasks_data:
    
        tasks.append(row["name"])
    
        time_history.append(row["duration"])

    # Combining tasks having same names

    unique_tasks = set(tasks)

    unique_tasks_duration = []

    for t in unique_tasks:

        index = 0

        duration = 0.0

        while index < len(tasks):

            if tasks[index] == t:

                duration += float(time_history[index])
            
            index += 1
        
        unique_tasks_duration.append(duration)
                
    return list(unique_tasks), unique_tasks_duration
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/history')
def history():
    return redirect(url_for('daily_history'))

@app.route('/insert')
def insert_task():
    print(request.args)
    if 'name' in request.args:
        task_name = request.args.get('name')
        return render_template('log.html', task_name = task_name)
    
    return render_template('task.html')

   
@app.route('/task_update')
def task_update():

    tasks_list, durations_list = get_task_history('Daily')
    
    if 'name' in request.args and 'duration' in request.args:
        task_name = request.args["name"]
        duration_parts = request.args["duration"].split(":")
        
        hours = int(duration_parts[0])
        minutes = int(duration_parts[1]) / 60
        duration = hours + minutes
        duration = f'{duration:.2f}'
        conn = sqlite3.connect('taskHistory.db')
        cur = conn.cursor()
        
        if task_name in tasks_list:
            old_duration = durations_list[tasks_list.index(task_name)]
            new_duration = old_duration + float(duration)
            cur.execute('UPDATE Task_History SET duration = ? WHERE name = ?' , (new_duration, task_name))
        else:
            cur.execute('INSERT INTO Task_History (name, duration, date) values (?,?,?)' , (request.args['name'] , duration, datetime.now().date()) )
        
        conn.commit()
        conn.close()

        return 'Task Updated.'
    
    return redirect(url_for('home'))


@app.route('/daily')
def daily_history():
    
    tasks, time_history = get_task_history('Daily')

    return render_template('history.html', status = 'Daily', tasks=tasks, time_history=time_history, bg_colors=bg_colors, borders=borders)

@app.route('/monthly')
def monthly_history():

    tasks, time_history = get_task_history('Monthly')

    return render_template('history.html', status = 'Monthly', tasks=tasks, time_history=time_history, bg_colors=bg_colors, borders=borders)

@app.route('/yearly')
def yearly_history():
    
    tasks, time_history = get_task_history('Yearly')

    return render_template('history.html', status = 'Yearly', tasks=tasks, time_history=time_history, bg_colors=bg_colors, borders=borders)

if __name__ == "__main__":
    create_task_table()
    app.run(debug=True)
