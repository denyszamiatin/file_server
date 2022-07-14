import hashlib

import config
from file_server import File, FileServerError


class  SignedFile(File):
	HASH_LENGTH = 32

	@staticmethod
	def _calculate_hash(content):
		md5 = hashlib.md5()
		md5.update(content)
		md5.update(config.get_secret_key())
		return md5.hexdigest().encode("utf-8")

	@staticmethod
	def create_file(data):
		return File.create_file(SignedFile._calculate_hash(data) + data)

	@staticmethod
	def read_file(filename):
		data = File.read_file(filename)
		hash_, content = data[:SignedFile.HASH_LENGTH], data[SignedFile.HASH_LENGTH:]
		if hash_ != SignedFile._calculate_hash(content):
			raise FileServerError("Integrity error")
		return content