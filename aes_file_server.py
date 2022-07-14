from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from file_server import File, FileServerError


class EncryptedFile(File):
	key = get_random_bytes(16)

	@staticmethod
	def create_file(data):
		cipher = AES.new(EncryptedFile.key, AES.MODE_EAX)
		ciphertext, tag = cipher.encrypt_and_digest(data)
		return File.create_file(cipher.nonce + tag + ciphertext)

	@staticmethod
	def read_file(filename):
		data = File.read_file(filename)
		nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
		cipher = AES.new(EncryptedFile.key, AES.MODE_EAX, nonce)
		try:
			return cipher.decrypt_and_verify(ciphertext, tag)
		except ValueError:
			raise FileServerError("Encryption error")