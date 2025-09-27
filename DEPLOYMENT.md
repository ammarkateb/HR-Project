# Deploy HR Project to Public URL

Your HR Project is now ready to deploy to a public URL that anyone can access. Here are 3 easy options:

## Option 1: Render (Recommended - Free)

1. Go to [render.com](https://render.com) and create a free account
2. Click "New +" → "Web Service"
3. Choose "Build and deploy from a Git repository"
4. Connect your GitHub account and create a new repository
5. Upload your HR Project files to that repository
6. Select the repository in Render
7. Render will automatically detect the `render.yaml` file and deploy
8. You'll get a public URL like: `https://hr-project-xyz.onrender.com`

**Pros:** Free forever, automatic deployments, custom domains available

## Option 2: Railway (Free)

1. Go to [railway.app](https://railway.app) and sign up
2. Click "Deploy from GitHub repo"
3. Upload your project to GitHub first
4. Connect and deploy
5. Get URL like: `https://hr-project-production.up.railway.app`

## Option 3: Heroku (Free tier limited)

1. Install Heroku CLI
2. Create a `Procfile` with: `web: gunicorn app:app`
3. Run these commands in your project folder:
   ```bash
   git init
   heroku create your-hr-project-name
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

## Quick GitHub Setup

If you need to put your code on GitHub first:

1. Go to [github.com](https://github.com) and create a new repository
2. In your HR Project folder, run:
   ```bash
   git init
   git add .
   git commit -m "Initial HR Project"
   git branch -M main
   git remote add origin https://github.com/yourusername/hr-project.git
   git push -u origin main
   ```

## What's Included for Deployment

✅ `render.yaml` - Render deployment configuration
✅ `requirements.txt` - Python dependencies
✅ `runtime.txt` - Python version specification
✅ Production-ready Flask app with environment port handling
✅ Gunicorn WSGI server for production

## Default Login for Public Site
- **Username:** admin
- **Password:** admin123

**Security Note:** Change the default credentials in `app.py` before deploying to production!