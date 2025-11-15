from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from datetime import datetime
from .scraper import get_top_100
from .spotify import SpotifyClient
from .utils import validate_date

routes = Blueprint("routes", __name__)

@routes.route("/", methods=["GET"])
def index():
    """Homepage with date form."""
    # Ustaw maksymalną datę na dzisiaj
    max_date = datetime.now().strftime("%Y-%m-%d")
    return render_template("index.html", max_date=max_date)

@routes.route("/start", methods=["POST"])
def start():
    """Validate date and begin Spotify OAuth."""
    user_date = request.form.get("date")
    playlist_name = request.form.get("playlist_name", "").strip()
    
    if not validate_date(user_date):
        flash("Invalid date format. Use YYYY-MM-DD.", "error")
        return redirect(url_for("routes.index"))

    # Save date and optional playlist name in session
    session["selected_date"] = user_date
    session["playlist_name"] = playlist_name if playlist_name else None

    # Redirect to Spotify login
    spotify = SpotifyClient()
    auth_url = spotify.get_auth_url()
    return redirect(auth_url)



@routes.route("/callback")
def callback():
    """Spotify redirects here with ?code=xxx."""
    code = request.args.get("code")

    if not code:
        flash("Authorization error: missing code.", "error")
        return redirect(url_for("routes.index"))

    spotify = SpotifyClient()
    spotify.fetch_token(code)  # Save access token in session

    return redirect(url_for("routes.create_playlist"))


@routes.route("/create_playlist")
def create_playlist():
    """Generate playlist from Billboard top 100."""
    user_date = session.get("selected_date")
    playlist_name = session.get("playlist_name")
    
    if not user_date:
        flash("Session expired. Please try again.", "error")
        return redirect(url_for("routes.index"))

        # Step 1: Scrape Billboard
    try:
        songs = get_top_100(user_date)
    except Exception:
        flash("Failed to fetch Billboard data.", "error")
        return redirect(url_for("routes.index"))

    spotify = SpotifyClient()

    # Step 2: Create playlist
    try:
        playlist_url = spotify.create_playlist_from_songs(user_date, songs, playlist_name)
    except Exception:
        flash("Spotify playlist creation failed.", "error")
        return redirect(url_for("routes.index"))

    return render_template("playlist_created.html", playlist_url=playlist_url)