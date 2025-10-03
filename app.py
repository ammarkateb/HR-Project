from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = 'hr_project_secret_key'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL',
    'postgresql://postgres.xanpxygpcbbcxejkqloa:ABDULKAREEMABDULRAHMANAMMAR@aws-1-eu-central-1.pooler.supabase.com:6543/postgres')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Create necessary directories
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('assets', exist_ok=True)

@app.route('/')
def login():
    response = render_template('login.html')
    return response

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']

    # Basic validation - you can replace this with actual authentication
    if username and password:
        # Accept any username/password for now
        return render_template('dashboard.html', username=username)
    else:
        flash('Please fill in both fields', 'error')
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/employees')
def employees():
    return render_template('employees.html')

@app.route('/add_employee', methods=['POST'])
def add_employee():
    # Get form data
    employee_data = {
        'first_name_ar': request.form.get('first_name_ar'),
        'second_name_ar': request.form.get('second_name_ar'),
        'third_name_ar': request.form.get('third_name_ar'),
        'last_name_ar': request.form.get('last_name_ar'),
        'first_name_en': request.form.get('first_name_en'),
        'second_name_en': request.form.get('second_name_en'),
        'third_name_en': request.form.get('third_name_en'),
        'last_name_en': request.form.get('last_name_en'),
        'employee_number': request.form.get('employee_number'),
        'national_identifier': request.form.get('national_identifier'),
        'birth_date': request.form.get('birth_date') if request.form.get('birth_date') else None,
        'birth_city': request.form.get('birth_city'),
        'blood_type_id': request.form.get('blood_type_id'),
        'nationality_id': request.form.get('nationality_id'),
        'religion_id': request.form.get('religion_id'),
    }

    # Validate required fields
    if not employee_data['employee_number'] or len(employee_data['employee_number']) != 10:
        flash('Employee number must be exactly 10 digits', 'error')
        return render_template('employees.html')

    if not employee_data['national_identifier'] or len(employee_data['national_identifier']) != 10:
        flash('National ID must be exactly 10 digits', 'error')
        return render_template('employees.html')

    if not employee_data['blood_type_id'] or not employee_data['nationality_id'] or not employee_data['religion_id']:
        flash('Please select all required fields', 'error')
        return render_template('employees.html')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO persons (
                first_name_ar, second_name_ar, third_name_ar, last_name_ar,
                first_name_en, second_name_en, third_name_en, last_name_en,
                employee_number, national_identifier, birth_date, birth_city,
                blood_type_id, nationality_id, religion_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            employee_data['first_name_ar'], employee_data['second_name_ar'],
            employee_data['third_name_ar'], employee_data['last_name_ar'],
            employee_data['first_name_en'], employee_data['second_name_en'],
            employee_data['third_name_en'], employee_data['last_name_en'],
            employee_data['employee_number'], employee_data['national_identifier'],
            employee_data['birth_date'], employee_data['birth_city'],
            employee_data['blood_type_id'], employee_data['nationality_id'],
            employee_data['religion_id']
        ))

        conn.commit()
        cur.close()
        conn.close()

        flash('Employee added successfully!', 'success')
        return render_template('employees.html')
    except Exception as e:
        flash(f'Error adding employee: {str(e)}', 'error')
        return render_template('employees.html')

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

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({
            'success': False,
            'message': 'Please fill in all fields'
        }), 400

    if len(username) < 3:
        return jsonify({
            'success': False,
            'message': 'Username must be at least 3 characters'
        }), 400

    if '@' not in email:
        return jsonify({
            'success': False,
            'message': 'Please enter a valid email'
        }), 400

    if len(password) < 6:
        return jsonify({
            'success': False,
            'message': 'Password must be at least 6 characters'
        }), 400

    # TODO: Add database integration to store user
    # For now, just return success
    return jsonify({
        'success': True,
        'message': f'Account created successfully! Please log in with your credentials.'
    }), 201

@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    # Get real employee count from database
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM persons")
        employee_count = cur.fetchone()[0]
        cur.close()
        conn.close()
    except:
        employee_count = 0

    dashboard_data = {
        'overview': {
            'employees': employee_count,
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