import dropbox
import os

import dbcheck
import stats

from flask import Flask, render_template 

TOKEN = os.environ['DB_TOKEN']
DEBUG = True

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = DEBUG


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html',
                           title='Home',
                           stats=stats_dict,
                           size=size_dict,)	


if __name__ == "__main__":

	dbx = dropbox.Dropbox(TOKEN)
	connection_result = dbcheck.check(dbx)
	stats_dict, size_dict = stats.dropbox_stats(dbx, "", testing_mode=DEBUG)

	app.run()


		