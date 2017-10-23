import dropbox

stats_dict = {}
size_dict = {}

def extension_type(item):
	"""finding extension 
	"""

	#Get the extension to know which bucket it belongs to
	if "." in item.name:
		location = item.name.rfind(".")
		#print("\n\tname: {}\n\textension: {}\n\tsize: {}\n".format(item.name, item.name[location:], item.size))
		return item.name[location:]

	return ".none"


def update_stats(ext_type, size, testing_mode=False):
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

	if testing_mode:
		print("\t{}".format(stats_dict))
		print("\t{}".format(size_dict))


def dropbox_stats(dbx, path, testing_mode=False):
	""" Gather stats for the Dropbox account. 
	"""
	try:
		dir_listing = dbx.files_list_folder(path)

		for item in dir_listing.entries:
			
			if type(item) == dropbox.files.FileMetadata: 
				#print(". {}".format(item.name))
				update_stats(extension_type(item), item.size, testing_mode)

			if type(item) == dropbox.files.FolderMetadata: 
				print("{}".format(item.path_display))
				if not testing_mode:
					dropbox_stats(dbx, item.path_display, testing_mode)
	except:		
		if path == "":
			path = "{folder root}"
		
		print("[!] Failed to return path {}".format(path))

	return stats_dict, size_dict
