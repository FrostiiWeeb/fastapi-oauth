from .errors import MissingParameter, OAuthError, HTTPError
from .scope import Scope
from .token import Token
from .user import User

import aiohttp
from typing import *

class Session(object):
	def __init__(self) -> None:
		self.session = None

	async def do_action(self, method, *args, **kwargs):
		self.session = aiohttp.ClientSession()
		method = getattr(self.session, method)
		res = await method(*args, **kwargs)
		return await res.json()

class OAuthSession(object):
	global DISCORD_API_FORMAT
	global DISCORD_API_URL
	DISCORD_API_URL = "https://discord.com/api/v8"
	DISCORD_API_FORMAT = "{}{}"
	def __init__(self, client_id : int, client_secret : str, redirect_uri : str, scope : Scope) -> None:
		self.client_id = client_id
		self.client_secret = client_secret
		self.redirect_uri = redirect_uri
		self.scope = scope
		self.refresh_token = None
		self.session = Session()

	async def _get_token(self, code : str = None):
		payload = {
			"client_id": self.client_id,
			"client_secret": self.client_secret,
			"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": self.redirect_uri,
			"scope": self.scope.scopes
		}
		headers = {"Content-Type": 'application/x-www-form-urlencoded'}
		url = DISCORD_API_FORMAT.format(DISCORD_API_URL, "/oauth2/token/")
		res = await self.session.do_action("post", url=url, data = payload, headers = headers)
		res.raise_for_status()
		json = await res.json()
		self.refresh_token = json.get("refresh_token")
		self.token_type = json.get("token_type")
		return Token(json.get("access_token"))


	async def get_token(self, code : str):
		return await self._get_token(code)

	async def _fetch_user(self, access_token: str):
		url = DISCORD_API_FORMAT.format(DISCORD_API_URL, "/users/@me")
		headers = {"Authorization": f"{self.token_type} {access_token}"}
		res = await self.session.do_action("get", url=url, headers = headers)
		json = await res.json()
		return User(json)

	async def fetch_user(self, access_token: str):
		return await self._fetch_user(access_token)

	async def _refresh_token(self):
		payload = {
			'client_id': self.client_id,
			'client_secret': self.client_secret,
			'grant_type': 'refresh_token',
			'refresh_token': self.refresh_token

		}
		headers = {"Content-Type": 'application/x-www-form-urlencoded'}
		url = DISCORD_API_FORMAT.format(DISCORD_API_URL, "/oauth2/token/")
		res = await self.session.do_action("post", url=url, data = payload, headers = headers)
		res.raise_for_status()
		json = await res.json()
		self.token_type = json.get("token_type")
		return Token(json.get("access_token"))