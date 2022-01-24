from fastapi.responses import RedirectResponse
from fastapi.datastructures import URL
from starlette.background import BackgroundTask

import typing

class Redirection(RedirectResponse):
	def __init__(self, url: typing.Union[str, URL], status_code: int = 307, headers: dict = None, background: BackgroundTask = None) -> None:
		super().__init__(url, status_code, headers, background)