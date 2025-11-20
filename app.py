# Import necessary libraries
from flask import Flask, redirect, request, session, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import datetime
import pytz
import requests
import os

app = Flask(__name__)
app.secret_key = "secret-key"

# Allow insecure local testing (HTTP instead of HTTPS)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Google OAuth Flow setup
flow = Flow.from_client_secrets_file(
    "credentials.json",
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid"
    ],
    redirect_uri="http://127.0.0.1:5000/oauth2callback"
)

# Home Page Setup
@app.route("/")
def index():
    if "google_id" in session:
        ist_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_ist = ist_time.strftime("%Y-%m-%d %H:%M:%S")

        return render_template(
            "home.html",
            name=session['name'],
            email=session['email'],
            picture=session['picture'],
            current_ist=current_ist
        )

    # If not logged in
    return render_template("login.html")

# Login
@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

# OAuth CallBack
@app.route("/oauth2callback")
def oauth2callback():
    flow.fetch_token(authorization_response=request.url)

    if session["state"] != request.args.get("state"):
        return "Error: State mismatch", 400

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    # Validate token and extract user info
    id_info = id_token.verify_oauth2_token(
        credentials._id_token,
        token_request,
        flow.client_config["client_id"]
    )

    # Store user info in session
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    session["picture"] = id_info.get("picture")

    return redirect("/")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Run main app
if __name__ == "__main__":
    app.run(debug=True)
