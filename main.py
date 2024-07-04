
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from time import strftime, localtime
from authlib.integrations.flask_client import OAuth
from functools import wraps
from utils.totp_functions import create_2fa_kps
import os

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function






app = Flask(__name__)

app.secret_key = os.urandom(24)

# OAuth Configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id= GOOGLE_CLIENT_ID, 
    client_secret= GOOGLE_CLIENT_SECRET, 
	server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'},
)


@app.route('/', methods=['GET', 'POST'])

def index():

	return render_template('base.html')

@app.route('/login')
def login():
    return google.authorize_redirect(url_for('authorize', _external=True))

@app.route('/login/callback')
def authorize():
    token = google.authorize_access_token()
    resp = resp = google.get('https://www.googleapis.com/oauth2/v3/userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

@app.route('/2fa', methods=['GET', 'POST'])
@login_required
def get_2fa():
	secrets_path = "config/secrets.json"
	all_kps = create_2fa_kps(secrets_path)
	if request.args.get('api') == "true":
		return jsonify(all_kps)

	return render_template('two_fa.html',kps= all_kps)

if __name__ == "__main__":
	app.run(debug=True)

