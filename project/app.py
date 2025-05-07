from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# In-memory storage (for simplicity)
users = {}
marriage_homes = []
feedbacks = []
bookings = []  # Store bookings here

# Home Route
@app.route("/")
def home():
    return render_template("login.html")

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users:
            flash("Username already exists!")
        else:
            users[username] = password
            flash("Registration successful! Please log in.")
            return redirect(url_for("home"))
    return render_template("register.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["user"] = username
            flash(f"Welcome, {username}!")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials. Please try again.")
    return render_template("login.html")

# Dashboard Route
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("dashboard.html", username=session["user"], marriage_homes=marriage_homes, bookings=bookings)

# Add Marriage Home Route
@app.route("/add-marriage-home", methods=["GET", "POST"])
def add_marriage_home():
    if "user" not in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        capacity = request.form.get("capacity")
        marriage_homes.append({"name": name, "location": location, "capacity": capacity})
        flash("Marriage home added successfully!")
        return redirect(url_for("dashboard"))
    return render_template("add_marriage_home.html")

# Feedback Route
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if "user" not in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        client_name = request.form.get("client_name")
        comments = request.form.get("comments")
        feedbacks.append({"client_name": client_name, "comments": comments})
        flash("Feedback submitted successfully!")
        return redirect(url_for("dashboard"))
    return render_template("feedback.html")

# Book Service Route
@app.route("/book-service/<int:home_id>", methods=["GET", "POST"])
def book_service(home_id):
    if "user" not in session:
        return redirect(url_for("home"))
    
    home = marriage_homes[home_id]
    
    if request.method == "POST":
        client_name = request.form.get("client_name")
        service_date = request.form.get("service_date")
        
        booking = {
            "client_name": client_name,
            "home": home["name"],
            "service_date": service_date,
            "status": "Booked"
        }
        
        bookings.append(booking)
        flash("Service booked successfully!")
        return redirect(url_for("dashboard"))
    
    return render_template("book_service.html", home=home)

# Logout Route
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

