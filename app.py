from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/insert', methods = ['POST', 'GET'])
def insert_task():

    if 'task_name' in request.args:
        task_name = request.args.get('task_name')
        return render_template('log.html', task_name = task_name)
    
    return render_template('task.html')


   

if __name__ == "__main__":

    app.run(debug=True)