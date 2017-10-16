import dropbox
import os


token = os.environ['DB_TOKEN']


def check_dropbox_sdk_init(db_object):
	try:
		basic_info = dbx.users_get_current_account()
		print("[*] Success. Connected to Dropbox API")
		return True
	except:
		print("[*] Fail. Unable to connect to Dropbox API. Did you set DB_TOKEN environment variable?")
		return False

	return False


def list_dropbox_folder(dbx, path):
	try:
		dir_listing = dbx.files_list_folder(path)
		for item in dir_listing.entries:
			print(item.path_display)
	except:
		if path == "":
			path = "{folder root}"
		print("[!] Failed to return path {}".format(path))


if __name__ == "__main__":

	dbx = dropbox.Dropbox(token)
	check_dropbox_sdk_init(dbx)
	list_dropbox_folder(dbx, "") #testing with root path ""



		