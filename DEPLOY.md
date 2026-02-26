# BookMyFlick Deployment Guide - Automatic Deploy

## Step 1: Push Code to GitHub (Do Once)

1. Go to https://github.com and create a new repository named "bookmyflick"
2. Initialize git and push your code:

```
bash
# Open terminal in your project folder
git init
git add .
git commit -m "Initial commit"

# Add your GitHub repo
git remote add origin https://github.com/natu031/BookMyFlick.git
git push -u origin main
```

## Step 2: Set Up Automatic Deploy on Render

1. Go to https://dashboard.render.com
2. Sign up/Login with your GitHub account
3. Click "New" → "Web Service"
4. Connect your GitHub repository "bookmyflick"
5. Configure:
   - **Name**: bookmyflick
   - **Region**: Choose closest to you  
   - **Branch**: main
   - **Build Command**: (leave empty)
   - **Start Command**: `gunicorn app:app`
6. **IMPORTANT -- Enable AutoDeploy**: 
   - Look for "Auto-Deploy" toggle and turn it ON
   - This makes every git push automatically deploy!
7. Click "Create Web Service"

## Step 3: Get Your URL
- After deployment (2-3 minutes), you'll get a URL like: `bookmyflick.onrender.com`
- Visit: https://dashboard.render.com to see your deployed site

## Step 4: Auto-Deploy Updates

Whenever you make changes to your code:

```
bash
git add .
git commit -m "Your changes description"
git push
```

Render will automatically deploy your changes! 🎉

---

## Files Ready for Auto-Deploy:
✅ app.py - main Flask application  
✅ Procfile - for Render.com
✅ requirements.txt - with gunicorn
✅ runtime.txt - Python version
✅ .gitignore - excluding unnecessary files
✅ templates/ - all HTML pages
✅ static/ - CSS and images
