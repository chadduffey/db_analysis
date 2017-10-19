import dropbox
import os


TOKEN = os.environ['DB_TOKEN']


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
		print("\textension: {}".format(item.name[location:]))
		return item.name[location:]

	return ".none"

def update_stats(ext_type):
	"""update the global dictionary that holds all the extension types.
	"""
	global stats_dict

	if len(ext_type) > 5:
		pass

	if ext_type in stats_dict:
		stats_dict[ext_type] += 1
	else:
		stats_dict[ext_type] = 1

	print(stats_dict)


def dropbox_stats(dbx, path):
	""" Gather stats for the Dropbox account. 
	"""
	try:
		dir_listing = dbx.files_list_folder(path)

		for item in dir_listing.entries:
			
			if type(item) == dropbox.files.FileMetadata: 
				#print(". {}".format(item.name))
				update_stats(extension_type(item))

			if type(item) == dropbox.files.FolderMetadata: 
				print("") 
				print("{}".format(item.path_display))
				dropbox_stats(dbx, item.path_display)
	except:		
		if path == "":
			path = "{folder root}"
		
		print("[!] Failed to return path {}".format(path))
	

if __name__ == "__main__":

	stats_dict = {}

	dbx = dropbox.Dropbox(TOKEN)
	check_dropbox_sdk_init(dbx)
	dropbox_stats(dbx, "")



		