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

def stats_update(stats, item):

	if "." in item:
		print(rfind("."))
	


def dropbox_stats(dbx, path):
	""" Gather stats for the Dropbox account. 
	"""

	content_stats = {	"pdf":0, 
						"docx":0,
						"xlsx":0,
						"pptx":0,
						"doc":0,
						"xls":0,
						"ppt":0,
						"exe":0,
						"iso":0,
						"jpg":0,
						"png":0,
						"other":0	}

	try:
		dir_listing = dbx.files_list_folder(path)

		for item in dir_listing.entries:
			
			if type(item) == dropbox.files.FileMetadata: 
				print(". {}".format(item.name))

			if type(item) == dropbox.files.FolderMetadata: 
				print("") 
				print("{}".format(item.path_display))
				dropbox_stats(dbx, item.path_display)
	except:		
		if path == "":
			path = "{folder root}"
		
		print("[!] Failed to return path {}".format(path))

	return content_stats


def delete_dot_git_folders(dbx, path, delete=False):
	""" Find, and optionally delete the .git folders in Dropbox
	"""
	try:
		dir_listing = dbx.files_list_folder(path)

		for item in dir_listing.entries:

			if type(item) == dropbox.files.FolderMetadata: 
				if item.name == ".git":
					delete_folder(dbx, item.path_display)
				else:
					delete_dot_git_folders(dbx, item.path_display)
	except:		
		if path == "":
			path = "{folder root}"
		
		print("[!] We failed on this one: {}".format(path))


def delete_folder(dbx, path):
	""" Delete a folder
	"""
	print("[!] Deleting folder: {}".format(path))
	result = dbx.files_delete(path)
	print(result)
	

if __name__ == "__main__":

	dbx = dropbox.Dropbox(TOKEN)
	check_dropbox_sdk_init(dbx)
	dropbox_stats(dbx, "")
	#delete_dot_git_folders(dbx, "")



		