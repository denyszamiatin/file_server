import ConfigParser

config = ConfigParser.ConfigParser()
config.read("file_server.ini")

def get_working_dir():
	return config.get("Directories", "working_dir")

def get_filename_length():
	return config.getint("Values", "filename_length")