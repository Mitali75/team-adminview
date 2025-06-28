from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

# -------------------------------
# Helper Functions
# -------------------------------
def load_feedbacks():
    with open('feedback_data.json', 'r') as f:
        return json.load(f)

def save_feedbacks(feedbacks):
    with open('feedback_data.json', 'w') as f:
        json.dump(feedbacks, f, indent=2)

# -------------------------------
# Admin Login
# -------------------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        with open('admin_credentials.json', 'r') as f:
            data = json.load(f)
        if request.form['password'] == data['password']:
            feedbacks = load_feedbacks()
            return render_template('dashboard.html', feedbacks=feedbacks)
        else:
            return render_template('login.html', error='Incorrect password')
    return render_template('login.html')


# -------------------------------
# Change Admin Password
# -------------------------------
@app.route('/admin/change-password', methods=['GET', 'POST'])
def change_password():
    message = None
    success = False
    if request.method == 'POST':
        with open('admin_credentials.json', 'r') as f:
            admin = json.load(f)

        old_pass = request.form['old_password']
        new_pass = request.form['new_password']
        confirm_pass = request.form['confirm_password']

        if old_pass != admin['password']:
            message = 'Old password is incorrect.'
        elif new_pass != confirm_pass:
            message = 'New passwords do not match.'
        else:
            admin['password'] = new_pass
            with open('admin_credentials.json', 'w') as f:
                json.dump(admin, f)
            message = 'Password changed successfully!'
            success = True

    return render_template('change_password.html', message=message, success=success)


# -------------------------------
# Delete a Feedback
# -------------------------------
@app.route('/admin/delete/<int:index>', methods=['POST'])
def delete_feedback(index):
    feedbacks = load_feedbacks()
    if 0 <= index < len(feedbacks):
        feedbacks.pop(index)
        save_feedbacks(feedbacks)
    return redirect(url_for('admin_login'))  # refresh dashboard


# -------------------------------
# Default route (optional redirect)
# -------------------------------
@app.route('/')
def home():
    return redirect(url_for('admin_login'))


# -------------------------------
# Run the app
# -------------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

