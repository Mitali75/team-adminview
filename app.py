from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

feedbacks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        "member": request.form['member'],
        "project": request.form['project'],
        "task": request.form['task'],
        "difficulty": request.form['difficulty'],
        "comments": request.form['comments'],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    feedbacks.append(data)
    return redirect('/success')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(debug=True, host="0.0.0.0", port=port)


