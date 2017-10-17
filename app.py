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


def list_dropbox_folders(dbx, path):
	""" List all the Dropbox folders
	"""
	try:
		dir_listing = dbx.files_list_folder(path)

		for item in dir_listing.entries:
			
			if type(item) == dropbox.files.FileMetadata: 
				print(". {}".format(item.name))

			if type(item) == dropbox.files.FolderMetadata: 
				print("") 
				print("{}".format(item.path_display))
				list_dropbox_folders(dbx, item.path_display)
	except:		
		if path == "":
			path = "{folder root}"
		
		print("[!] Failed to return path {}".format(path))


def find_dot_git_folders(dbx, path, delete=False):
	""" Find, and optionally delete the .git folders in Dropbox
	"""
	try:
		dir_listing = dbx.files_list_folder(path)

		for item in dir_listing.entries:

			if type(item) == dropbox.files.FolderMetadata: 
				if item.name == ".git":
					print("") 
					print("{}".format(item.path_display))
				find_dot_git_folders(dbx, item.path_display)
	except:		
		if path == "":
			path = "{folder root}"
		
		print("[!] Failed to return path {}".format(path))


if __name__ == "__main__":

	dbx = dropbox.Dropbox(TOKEN)
	check_dropbox_sdk_init(dbx)
	#list_dropbox_folders(dbx, "")
	find_dot_git_folders(dbx, "")



		