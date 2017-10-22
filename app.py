import dropbox
import os

from flask import Flask 	

TOKEN = os.environ['DB_TOKEN']
DEBUG = True

app = Flask(__name__)

def check_dropbox_sdk_init(db_object):
	""" Quick check to make sure we successfully initialized a Dropbox object. 
	"""
	try:
		db_object.users_get_current_account()
		print("[*] Success. Connected to Dropbox API")
		return True
	except:
		print("[*] Fail. Unable to connect to Dropbox API. Did you set DB_TOKEN environment variable?")
		return False

	return False

def extension_type(item):
	"""finding extension 
	"""

	#Get the extension to know which bucket it belongs to
	if "." in item.name:
		location = item.name.rfind(".")
		print("\n\tname: {}\n\textension: {}\n\tsize: {}\n".format(item.name, item.name[location:], item.size))
		return item.name[location:]

	return ".none"

def update_stats(ext_type, size):
	"""update the global dictionary that holds all the extension types.
	"""
	global stats_dict
	global size_dict

	if len(ext_type) > 5:
		pass

	if ext_type in stats_dict:
		stats_dict[ext_type] += 1
		size_dict[ext_type] += size
	else:
		stats_dict[ext_type] = 1
		size_dict[ext_type] = size

	print("\t{}".format(stats_dict))
	print("\t{}".format(size_dict))


def dropbox_stats(dbx, path):
	""" Gather stats for the Dropbox account. 
	"""
	try:
		dir_listing = dbx.files_list_folder(path)

		for item in dir_listing.entries:
			
			if type(item) == dropbox.files.FileMetadata: 
				#print(". {}".format(item.name))
				update_stats(extension_type(item), item.size)

			if type(item) == dropbox.files.FolderMetadata: 
				print("") 
				print("{}".format(item.path_display))
				dropbox_stats(dbx, item.path_display)
	except:		
		if path == "":
			path = "{folder root}"
		
		print("[!] Failed to return path {}".format(path))


@app.route('/')
def hello_world():
	return "Ready to do Dropbox things with token: " + str(TOKEN)	

if __name__ == "__main__":

	stats_dict = {}
	size_dict = {}

	#start flask app
	app.run()


	dbx = dropbox.Dropbox(TOKEN)
	check_dropbox_sdk_init(dbx)
	#dropbox_stats(dbx, "")




		