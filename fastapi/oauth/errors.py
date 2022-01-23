import typing
from discord import HTTPException

class HTTPError(HTTPException):
	"""Raised upon an HTTP error"""
	pass

class OAuthError(Exception):
	"""Base class for most exceptions"""
	def __init__(self, arg : str, reason : str, code : int) -> None:
		super().__init__("{} (error code: {}): {}".format(reason, code, arg))

class MissingParameter(OAuthError):
	"""Raised upon not retreiving a parameter"""
	pass