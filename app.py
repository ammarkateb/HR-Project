from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from datetime import datetime

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

# API Endpoints for Mobile App
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        if username == 'admin' and password == 'admin123':
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'username': username,
                    'role': 'Administrator'
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
    else:
        return jsonify({
            'success': False,
            'message': 'Please fill in both fields'
        }), 400

@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    # Mock dashboard data
    dashboard_data = {
        'overview': {
            'employees': 156,
            'departments': 12,
            'pending_requests': 8,
            'active_projects': 24
        },
        'recent_activities': [
            {
                'id': 1,
                'title': 'New employee onboarded',
                'subtitle': 'John Doe joined the Engineering team',
                'time': '2 hours ago',
                'icon': 'person_add'
            },
            {
                'id': 2,
                'title': 'Leave request approved',
                'subtitle': 'Sarah Wilson\'s vacation request',
                'time': '4 hours ago',
                'icon': 'check_circle'
            },
            {
                'id': 3,
                'title': 'Performance review completed',
                'subtitle': 'Q3 reviews for Marketing team',
                'time': '1 day ago',
                'icon': 'star'
            },
            {
                'id': 4,
                'title': 'Training session scheduled',
                'subtitle': 'Leadership workshop next week',
                'time': '2 days ago',
                'icon': 'school'
            }
        ]
    }
    return jsonify(dashboard_data)

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("HR Project server starting...")
    print("Default login: admin / admin123")

    # Use PORT environment variable for deployment, fallback to 5000 for local
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)