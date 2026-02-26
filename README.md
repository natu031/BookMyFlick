# BookMyFlick 🎬

A BookMyShow clone for college project - Movie ticket booking website.

## Quick Deploy to GitHub

Run these commands in your project folder (Terminal):

```
bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/natu031/BookMyFlick.git
git push -u origin main
```

## Then Deploy to Render.com

1. Go to https://dashboard.render.com
2. Login with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repo "BookMyFlick"
5. Settings:
   - Name: bookmyflick
   - Branch: main
   - Start Command: `gunicorn app:app`
6. **Turn ON Auto-Deploy**
7. Click Create!

## Features
- Browse movies
- User login/signup
- Book seats
- Payment (mock)
- Dashboard with bookings
- Admin panel

## Tech Stack
- Python (Flask)
- SQLite database
- HTML/CSS/JS
