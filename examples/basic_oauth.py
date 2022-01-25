from fastapi import FastAPI
import uvicorn
from fastapi.oauth import OAuth2Session
from fastapi.oauth import Scope

app = FastAPI()

client = OAuth2Session(
	CLIENT_ID, "CLIENT_SECRET", "REDIRECT_URI", Scope(...) # it can be None too or not specify it)
)

@app.get("/redirect")
async def red():
	return await client.redirect()

uvicorn.run(app)