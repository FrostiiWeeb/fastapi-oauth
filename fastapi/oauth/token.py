from typing import *
from datetime import datetime

class Token(object):
	def __init__(self, token : str, expires_in : int) -> None:
		self.token = token
		self.expires_in = expires_in