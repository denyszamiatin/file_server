"""
Helper functions
"""

import random
import string
import config

def get_random_name(length=config.get_filename_length(), random=random):
    """
	Generate random string from ASCII lowercase and digits
    """
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
