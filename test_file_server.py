import string
import os
import pytest
import util

from file_server import File, FileServerError, handle_os_error
from signed_file_server import SignedFile
from aes_file_server import EncryptedFile


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
	@handle_os_error
	def f():
		raise OSError("Decorator test")
	with pytest.raises(FileServerError):
		f()


def test_chg_dir_if_exists():
	current_dir = os.getcwd()
	assert File.chg_dir("/") == "/", "Existing dir is not changed"
	os.chdir(current_dir)


def test_chg_dir_if_not_exists():
	NEW_DIR = "__test_folder__"
	current_dir = os.getcwd()
	assert File.chg_dir(NEW_DIR) == os.path.join(current_dir, NEW_DIR), "Dir is not created"
	os.chdir(current_dir)
	os.rmdir(NEW_DIR)


def test_create_and_read_file():
	filename = File.create_file(b"Hello")
	assert File.read_file(filename) == b"Hello", "File: Create or read doesn't work"
	os.remove(filename)


def test_del_file():
	filename = File.create_file(b"Hello")
	File.del_file(filename)
	assert not os.path.isfile(filename), "Delete doesn't work"


def test_get_metadata():
	filename = File.create_file(b"Hello")
	metadata = File.get_metadata(filename)
	assert metadata['size'] == len(b"Hello") and 'date' in metadata, "Get metadata doesn't work"
	os.remove(filename)


def test_list_files():
	filename = File.create_file(b"Hello")
	assert filename in File.list_files(), "List files doesn't work"
	os.remove(filename)


def test_signed_create_and_read_file():
	filename = SignedFile.create_file(b"Hello")
	assert SignedFile.read_file(filename) == b"Hello", "SignedFlie: Create or read doesn't work"
	os.remove(filename)


def test_signed_create_and_read_file_integrity_error():
	filename = SignedFile.create_file(b"Hello")
	with open(filename, "ab") as f:
		f.write(b"!")
	with pytest.raises(FileServerError):
		SignedFile.read_file(filename)
	os.remove(filename)


def test_encrypted_create_and_read_file():
	filename = EncryptedFile.create_file(b"Hello")
	assert EncryptedFile.read_file(filename) == b"Hello", "EncryptedFlie: Create or read doesn't work"
	os.remove(filename)


def test_encrypted_create_and_read_file_integrity_error():
	filename = EncryptedFile.create_file(b"Hello")
	with open(filename, "ab") as f:
		f.write(b"!")
	with pytest.raises(FileServerError):
		EncryptedFile.read_file(filename)
	os.remove(filename)

