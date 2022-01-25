from fastapi import FastAPI
import uvicorn
from fastapi.oauth import OAuth2Session
from fastapi.oauth import Scope

app = FastAPI()

client = OAuth2Session()