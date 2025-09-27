# HR Project

A Python Flask web application for HR management with a clean login interface.

## Features
- Login page with username/password authentication
- Clean, professional design using specified color scheme
- Dashboard view after successful login
- Logo placeholder for future branding

## Color Scheme
- **#4B504A** → Dark gray (headers, primary text)
- **#528049** → Medium green (accents, buttons)
- **#264F1B** → Dark green (hover states)
- **#9EA49C** → Light gray (background)

## Setup Instructions

1. Install Flask:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   cd ~/Desktop/"HR Project"
   python app.py
   ```

3. Open your browser and go to: `http://localhost:5000`

## Default Login Credentials
- **Username:** admin
- **Password:** admin123

## Project Structure
```
HR Project/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── login.html     # Login page
│   └── dashboard.html # Dashboard after login
├── static/            # Static files (CSS, JS)
├── assets/            # Logo and image files
└── README.md          # This file
```

## Adding Your Logo
Place your logo file in the `assets/` folder and update the logo placeholder in the HTML templates.