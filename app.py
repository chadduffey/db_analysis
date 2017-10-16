import dropbox
import os

token = os.environ['DB_TOKEN']

if __name__ == "__main__":

	try:
		dbx = dropbox.Dropbox(token)
		print(dbx.users_get_current_account())
	except:
		print("Unable to initialize Dropbox client. Did you remember to add DB_TOKEN environment variable?")
		exit()