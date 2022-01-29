from typing import *

class Scope(object):
	def __init__(self, scopes : List[str]) -> None:
		self._scopes = "%20".join(scopes)
		self.scope = self._scopes
		self.__scopes = scopes

	@property
	def scopes(self):
		return self._scopes

	def __repr__(self) -> str:
		return "<Scope {}>".format(" ".join([self.scopes]))