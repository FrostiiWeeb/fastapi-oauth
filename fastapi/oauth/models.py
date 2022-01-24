from .scope import Scope
from .session import OAuth2Session

from typing import *

class URL(object):
	def __init__(self, session : OAuth2Session, oauth_scope : Scope = None) -> None:
		self.url = None
		self.oauth_scope = oauth_scope
		self.session : OAuth2Session = session

	def __str__(self) -> str:
		return self.__repr__()

	def __repr__(self) -> str:
		return f"https://discord.com/oauth2/authorize?client_id={self.session.client_id}&redirect_uri={self.session.redirect_uri}&response_type=code&scope={self.oauth_scope.scope}" if self.oauth_scope else f"https://discord.com/oauth2/authorize?client_id={self.session.client_id}&redirect_uri={self.session.redirect_uri}&response_type=code"