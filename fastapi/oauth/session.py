from .errors import MissingParameter, OAuthError, HTTPError
from .scope import Scope
from .token import Token
from .user import User
from .responses import Redirection
from .models import URL

import aiohttp
import asyncio
import contextlib
from typing import *
from threading import Thread, Event
from discord.utils import sleep_until
from datetime import timedelta, datetime

class Session(object):
	def __init__(self) -> None:
		self.session = self

	async def do_action(self, method, *args, **kwargs):
		self.session = aiohttp.ClientSession()
		method = getattr(self.session, method)
		res = await method(*args, **kwargs)
		return await res.json()

class OAuth2Session(object):
	"""
	A OAuth2 Session for the discord API. Uses the `Bearer` authentication type.
	"""
	global DISCORD_API_FORMAT
	global DISCORD_API_URL
	DISCORD_API_URL = "https://discord.com/api/v8"
	DISCORD_API_FORMAT = "{}{}"
	def __init__(self, client_id : int, client_secret : str, redirect_uri : str, scope : Optional[Scope] = None) -> None:
		self.client_id = client_id
		self.client_secret = client_secret
		self.redirect_uri = redirect_uri
		self.scope = scope
		self.refresh_token = None
		self.expires_in = 0.0
		self._ev = Event()
		self._aev = asyncio.Event()
		self.session = Session()

	async def start_wait(self):
		try:
			time = datetime.utcnow() + timedelta(seconds=self.expires_in-10)
			await sleep_until(time)
			await self.refresh()
			await self.start_wait()
		except KeyboardInterrupt:
			return None

	async def redirect(self):
		url = URL(self, self.scope)
		res : aiohttp.ClientResponse = await self.session.do_action("get", url=str(url))
		await self.session.session.close()
		return Redirection(str(url))

	async def check_for_status(self, response : aiohttp.ClientResponse, message : str):
		if not response.status in (200, 201):
			raise HTTPError(response, message)
		return True

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
		json = await res.json()
		self.refresh_token = json.get("refresh_token")
		self.token_type = json.get("token_type")
		self.expires_in = int(json.get("expires_in"))
		self.token = Token(json.get("access_token"), self.expires_in)
		return await self.start_wait()


	async def get_token(self, code : str):
		return await self._get_token(code)

	async def _fetch_user(self, access_token: str) -> User:
		url = DISCORD_API_FORMAT.format(DISCORD_API_URL, "/users/@me")
		headers = {"Authorization": f"{self.token_type} {access_token}"}
		res = await self.session.do_action("get", url=url, headers = headers)
		json = await res.json()
		return User(json)

	async def fetch_user(self, access_token: str) -> User:
		return await self._fetch_user(access_token)

	async def _refresh_token(self):
		if not self.refresh_token:
			raise OAuthError("Please run the `{}` coroutine".format(self.get_token.__name__), "self.refresh_token not set", 1)
		payload = {
			'client_id': self.client_id,
			'client_secret': self.client_secret,
			'grant_type': 'refresh_token',
			'refresh_token': self.refresh_token

		}
		headers = {"Content-Type": 'application/x-www-form-urlencoded'}
		url = DISCORD_API_FORMAT.format(DISCORD_API_URL, "/oauth2/token/")
		res : aiohttp.ClientResponse = await self.session.do_action("post", url=url, data = payload, headers = headers)
		json = await res.json()
		self.refresh_token = json.get("refresh_token")
		self.token_type = json.get("token_type")
		self.expires_in = int(json.get("expires_in"))
		self.token = Token(json.get("access_token"))
		return self.token

	async def refresh(self):
		return await self._refresh_token()