from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "bookmyflick_secret_key_123"

# Use absolute path for SQLite database (works on Render)
instance_path = os.path.join(os.path.dirname(__file__), 'instance')
os.makedirs(instance_path, exist_ok=True)
db_path = os.path.join(instance_path, 'database.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Prevent browser caching
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# =====================
# DATABASE MODELS
# =====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_name = db.Column(db.String(100), nullable=False)
    show_time = db.Column(db.String(50), nullable=False)
    seats = db.Column(db.String(200), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="Confirmed")

# =====================
# MOVIES DATA - Using TMDB Images
# =====================

MOVIES = [
    {"id": 1, "name": "Avengers: Endgame", "image": "/static/movies/1.svg", "rating": "⭐ 8.4", "price": 250, "language": "English", "duration": 181},
    {"id": 2, "name": "Spider-Man: No Way Home", "image": "/static/movies/2.svg", "rating": "⭐ 8.2", "price": 200, "language": "English", "duration": 148},
    {"id": 3, "name": "Doctor Strange 2", "image": "/static/movies/3.svg", "rating": "⭐ 7.5", "price": 220, "language": "English", "duration": 126},
    {"id": 4, "name": "The Batman", "image": "/static/movies/4.svg", "rating": "⭐ 7.8", "price": 230, "language": "English", "duration": 176},
    {"id": 5, "name": "Top Gun: Maverick", "image": "/static/movies/5.svg", "rating": "⭐ 8.3", "price": 240, "language": "English", "duration": 131},
    {"id": 6, "name": "Jurassic World", "image": "/static/movies/6.svg", "rating": "⭐ 7.0", "price": 200, "language": "English", "duration": 147},
    {"id": 7, "name": "Oppenheimer", "image": "/static/movies/7.svg", "rating": "⭐ 8.4", "price": 280, "language": "English", "duration": 180},
    {"id": 8, "name": "Barbie", "image": "/static/movies/8.svg", "rating": "⭐ 7.8", "price": 250, "language": "English", "duration": 114},
    {"id": 9, "name": "Dune: Part Two", "image": "/static/movies/9.svg", "rating": "⭐ 8.6", "price": 270, "language": "English", "duration": 166},
    {"id": 10, "name": "Jawan", "image": "/static/movies/10.svg", "rating": "⭐ 7.5", "price": 180, "language": "Hindi", "duration": 169},
    {"id": 11, "name": "Animal", "image": "/static/movies/11.svg", "rating": "⭐ 7.2", "price": 170, "language": "Hindi", "duration": 201},
    {"id": 12, "name": "Pathaan", "image": "/static/movies/12.svg", "rating": "⭐ 7.3", "price": 175, "language": "Hindi", "duration": 146},
    {"id": 13, "name": "Leo", "image": "/static/movies/13.svg", "rating": "⭐ 7.4", "price": 185, "language": "Tamil", "duration": 165},
    {"id": 14, "name": "Mission: Impossible 7", "image": "/static/movies/14.svg", "rating": "⭐ 7.8", "price": 260, "language": "English", "duration": 163},
    {"id": 15, "name": "Fast X", "image": "/static/movies/15.svg", "rating": "⭐ 7.2", "price": 240, "language": "English", "duration": 141},
]

EVENTS = [
    {"id": 1, "name": "Music Festival 2024", "date": "SAT, MAR 15", "location": "Palace Grounds, Bengaluru", "image": "https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=400", "price": 1500},
    {"id": 2, "name": "Stand Up Comedy Night", "date": "SUN, MAR 20", "location": "Comics Club, Bengaluru", "image": "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=400", "price": 500},
    {"id": 3, "name": "Photography Workshop", "date": "SAT, MAR 25", "location": "Art Center, Bengaluru", "image": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=400", "price": 1000},
]

SPORTS = [
    {"id": 1, "name": "IPL 2024 - MI vs CSK", "date": "SAT, MAR 23", "location": "Wankhede Stadium, Mumbai", "image": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=400", "price": 2500, "sport": "Cricket"},
    {"id": 2, "name": "IPL 2024 - RCB vs DC", "date": "SUN, MAR 24", "location": "M. Chinnaswamy Stadium, Bengaluru", "image": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400", "price": 2200, "sport": "Cricket"},
]

THEATERS = [
    {"id": 1, "name": "PVR Cinemas", "location": "Mall of Asia", "price": 250, "available": 45},
    {"id": 2, "name": "INOX", "location": "Express Avenue", "price": 220, "available": 30},
    {"id": 3, "name": "Cinepolis", "location": "Phoenix Marketcity", "price": 200, "available": 50},
]

# =====================
# ROUTES
# =====================

@app.route("/")
def home():
    return render_template("index_new.html", movies=MOVIES)

# MOVIE DETAILS
@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    movie = next((m for m in MOVIES if m["id"] == movie_id), MOVIES[0])
    return render_template("movie_details.html", movie=movie, theaters=THEATERS)

# EVENTS
@app.route("/events")
def events():
    return render_template("events.html", events=EVENTS)

# PLAYS
@app.route("/plays")
def plays():
    return render_template("plays.html")

# SPORTS
@app.route("/sports")
def sports():
    return render_template("sports.html", sports=SPORTS)

# ACTIVITIES
@app.route("/activities")
def activities():
    return render_template("activities.html")

# SEARCH
@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    results = [m for m in MOVIES if query in m["name"].lower()]
    return render_template("search.html", movies=results, query=query)

# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return render_template("signup.html", error="Username or email already exists!")
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("signup.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials!")
    return render_template("login.html")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    
    user = User.query.get(session["user_id"])
    bookings = Booking.query.filter_by(user_id=session["user_id"]).all()
    return render_template("dashboard.html", user=user, bookings=bookings)

# SELECT SEATS
@app.route("/seats/<int:movie_id>")
def seats(movie_id):
    if "user_id" not in session:
        return redirect("/login")
    
    movie = next((m for m in MOVIES if m["id"] == movie_id), MOVIES[0])
    return render_template("seats.html", movie=movie, movie_id=movie_id)

# BOOK SEATS (API)
@app.route("/book", methods=["POST"])
def book():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Please login first!"})
    
    data = request.get_json()
    movie_name = data.get("movie_name")
    show_time = data.get("show_time")
    seats = data.get("seats")
    total_price = data.get("total_price")
    
    booking = Booking(
        user_id=session["user_id"],
        movie_name=movie_name,
        show_time=show_time,
        seats=seats,
        total_price=total_price
    )
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({"success": True, "booking_id": booking.id})

# PAYMENT
@app.route("/payment")
def payment():
    if "user_id" not in session:
        return redirect("/login")
    
    movie_name = request.args.get("movie_name", "")
    show_time = request.args.get("show_time", "")
    seats = request.args.get("seats", "")
    total_price = request.args.get("total_price", "0")
    
    return render_template("payment.html", 
                         movie_name=movie_name, 
                         show_time=show_time,
                         seats=seats,
                         total_price=total_price)

# BOOK CONFIRM
@app.route("/book_confirm")
def book_confirm():
    if "user_id" not in session:
        return redirect("/login")
    
    movie_name = request.args.get("movie_name")
    show_time = request.args.get("show_time")
    seats = request.args.get("seats")
    total_price = request.args.get("total_price")
    
    if not movie_name or not seats:
        return redirect("/")
    
    booking = Booking(
        user_id=session["user_id"],
        movie_name=movie_name,
        show_time=show_time,
        seats=seats,
        total_price=int(total_price) if total_price else 0
    )
    db.session.add(booking)
    db.session.commit()
    
    return redirect(f"/confirmation/{booking.id}")

# BOOKING CONFIRMATION
@app.route("/confirmation/<int:booking_id>")
def confirmation(booking_id):
    if "user_id" not in session:
        return redirect("/login")
    
    booking = Booking.query.get(booking_id)
    if not booking or booking.user_id != session["user_id"]:
        return redirect("/dashboard")
    
    return render_template("confirmation.html", booking=booking)

# ADMIN
@app.route("/admin")
def admin():
    if "username" not in session or session.get("username") != "admin":
        return redirect("/login")
    
    bookings = Booking.query.all()
    users = User.query.all()
    return render_template("admin.html", bookings=bookings, users=len(users))

# CANCEL BOOKING
@app.route("/cancel/<int:booking_id>")
def cancel_booking(booking_id):
    if "user_id" not in session:
        return redirect("/login")
    
    booking = Booking.query.get(booking_id)
    if booking and booking.user_id == session["user_id"]:
        booking.status = "Cancelled"
        db.session.commit()
    
    return redirect("/dashboard")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =====================
# CREATE DATABASE TABLES
# =====================
with app.app_context():
    db.create_all()

# =====================
# RUN APP
# =====================

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
