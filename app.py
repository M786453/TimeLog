from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def create_task_table():
    conn = sqlite3.connect('taskHistory.db')
    conn.execute('CREATE TABLE IF NOT EXISTS Task_History(task_name TEXT , task_duration INTEGER)')

    conn.commit()
    conn.close()


@app.route('/')
def home():
    
    return render_template('index.html')

@app.route('/insert', methods = ['POST', 'GET'])
def insert_task():

    if 'task_name' in request.args:
        task_name = request.args.get('task_name')
        return render_template('log.html', task_name = task_name)
    
    return render_template('task.html')
   
@app.route('/task_done')
def task_done():
    if 'task_name' in request.args and 'task_duration' in request.args:
        conn = sqlite3.connect('taskHistory.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO Task_History (task_name, task_duration) values (?,?)' , (request.args['task_name'] , request.args['task_duration']) )
        conn.commit()
        conn.close()
    return "task_done"


if __name__ == "__main__":
    create_task_table()
    app.run(debug=True)
