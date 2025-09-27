from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'hr_project_secret_key'

# Create necessary directories
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('assets', exist_ok=True)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']

    # Basic validation - you can replace this with actual authentication
    if username and password:
        if username == 'admin' and password == 'admin123':
            flash('Login successful!', 'success')
            return render_template('dashboard.html', username=username)
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')
    else:
        flash('Please fill in both fields', 'error')
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    print("HR Project server starting...")
    print("Default login: admin / admin123")

    # Use PORT environment variable for deployment, fallback to 5000 for local
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)