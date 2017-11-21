import dropbox
from flask import abort, Flask, redirect, request, session, url_for, render_template
from dropbox import DropboxOAuth2Flow
import os
import requests
import sys

import dbcheck
import stats

TOKEN = os.environ.get('DB_TOKEN')
DEBUG = True

WEBSERVER = "http://localhost:5000"

app = Flask(__name__)
app.secret_key = 'ChangeThisToSomethingRandom'

#app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = DEBUG

APP_KEY = 'nmn3f95z152pmbs'
APP_SECRET = os.environ.get('APP_SECRET')

REDIRECT_URI = "http://localhost:5000/dropbox-auth-finish"

def get_dropbox_auth_flow(web_app_session):
    return DropboxOAuth2Flow(APP_KEY, APP_SECRET, REDIRECT_URI,
                             web_app_session, "dropbox-auth-csrf-token")

@app.route('/dropbox-auth-start')
def dropbox_auth_start(web_app_session=session, request=request):
    authorize_url = get_dropbox_auth_flow(web_app_session).start()
    return redirect(authorize_url)

@app.route('/dropbox-auth-finish')
def dropbox_auth_finish():
    #struggling with the SDK, hacking this in for now

    try:
        finish_dict = {}
        finish_dict["code"] = request.args["code"]
        finish_dict["grant_type"] = 'authorization_code'
        finish_dict["client_id"] = APP_KEY
        finish_dict["client_secret"] = APP_SECRET
        finish_dict["redirect_uri"] = REDIRECT_URI

        r = requests.post('https://api.dropboxapi.com/oauth2/token', data=finish_dict)

        print(r.text)

        session["logged_in_to_dropbox"] = True
        return redirect('/')
        #with sdk it is meant to be like this:
        #access_token, user_id, url_state = get_dropbox_auth_flow(session).finish(finish_dict)
    
    except:
        return "something is broken"

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
	if "logged_in_to_dropbox" in session:
		#return render_template('index.html',title='Home', stats=stats_dict, size=size_dict,)
		return render_template('index.html', title='Welcome')
	else:
		#log them in
		return render_template('index.html', title='Log In!')

if __name__=='__main__':
	app.run(debug=True)

'''
if __name__ == "__main__":
    dbx = dropbox.Dropbox(TOKEN)
    connection_result = dbcheck.check(dbx)
    stats_dict, size_dict = stats.dropbox_stats(dbx, "", testing_mode=DEBUG)

    app.run()
'''

		