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

def get_dropbox_auth_flow(web_app_session):
    redirect_uri = WEBSERVER + "/dropbox-auth-finish"
    return DropboxOAuth2Flow(
        APP_KEY, APP_SECRET, redirect_uri, web_app_session,
        "dropbox-auth-csrf-token")

@app.route('/dropbox-auth-start')
def dropbox_auth_start(web_app_session=session, request=request):
    authorize_url = get_dropbox_auth_flow(web_app_session).start()
    print(authorize_url) #----
    return redirect(authorize_url)

@app.route('/dropbox-auth-finish')
def dropbox_auth_finish(web_app_session=session, request=request):
    print("finish") #-----------
    try:
        oauth_result = \
                get_dropbox_auth_flow(web_app_session).finish(
                    request.query_params)
        print("success")
    
    except:
        # Start the auth flow again.
        print(sys.exc_info()[0])
        return redirect("/dropbox-auth-start")

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
	if "logged_in_to_dropbox" in session:
		#return render_template('index.html',title='Home', stats=stats_dict, size=size_dict,)
		return render_template('index.html', title='Welcome')
	else:
		#log them in
		print("session: {}".format(session))
		print(request)
		return render_template('index.html', title='test')

if __name__=='__main__':
	app.run(debug=True)

'''
if __name__ == "__main__":
    dbx = dropbox.Dropbox(TOKEN)
    connection_result = dbcheck.check(dbx)
    stats_dict, size_dict = stats.dropbox_stats(dbx, "", testing_mode=DEBUG)

    app.run()
'''

		