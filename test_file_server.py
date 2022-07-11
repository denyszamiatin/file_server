import string
import os
import pytest
import util
import file_srv


@pytest.fixture
def name_length():
	return 10


def test_get_random_name_length_and_content(name_length):
	name = util.get_random_name(length=name_length)
	assert len(name) == name_length, "Name length is not correct"
	for c in name:
		assert c in string.ascii_lowercase + string.digits, "Restricted character in name"


def test_get_random_name_mock_random(name_length):
	class MockRandom:
		def choice(self, seq):
			return "a"

	name = util.get_random_name(length=name_length, random=MockRandom())
	assert name == "a"*name_length, "Random choice doesn't work"

def test_handle_os_error():
	@file_srv.handle_os_error
	def f():
		raise OSError("Decorator test")
	with pytest.raises(file_srv.FileServerError):
		f()


def test_chg_dir_if_exists():
	current_dir = os.getcwd()
	assert file_srv.chg_dir("/") == "/", "Existing dir is not changed"
	os.chdir(current_dir)


def test_chg_dir_if_not_exists():
	NEW_DIR = "__test_folder__"
	current_dir = os.getcwd()
	assert file_srv.chg_dir(NEW_DIR) == os.path.join(current_dir, NEW_DIR), "Dir is not created"
	os.chdir(current_dir)
	os.rmdir(NEW_DIR)

def test_create_and_read_file():
	filename = file_srv.create_file("Hello")
	assert file_srv.read_file(filename) == "Hello", "Create or read doesn't work"
	os.remove(filename)

def test_del_file():
	filename = file_srv.create_file("Hello")
	file_srv.del_file(filename)
	assert not os.path.isfile(filename), "Delete doesn't work"

def test_get_metadata():
	filename = file_srv.create_file("Hello")
	metadata = file_srv.get_metadata(filename)
	assert metadata['size'] == len("Hello") and 'date' in metadata, "Get metadata doesn't work"
	os.remove(filename)

def test_list_files():
	filename = file_srv.create_file("Hello")
	assert filename in file_srv.list_files(), "List files doesn't work"
	os.remove(filename)

